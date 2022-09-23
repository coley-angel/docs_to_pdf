import jinja2
from weasyprint import HTML, CSS
import os
import yaml
import markdown
from datetime import date
import logging
import argparse
import logging
import sys
from Loader_class import Loader
from collections.abc import Iterable
logger = logging.getLogger()

class CreatePdfFromDocs:
    def __init__(self, doc_folders='docs', output_dir='results', 
                 template_dir='templates', variable_dir='variables',
                 base_yml="meta_data.yml", template_base="index.html", 
                 date_fmt="%m.%d.%Y"):
        self.str_out = f"('{doc_folders}', '{output_dir}', '{template_dir}', '{variable_dir}', '{base_yml}', '{template_base}', '{date_fmt}')"
        self.py_path = self.get_abs_path_directory(__file__)
        self.result_path = os.path.join(self.py_path, output_dir)
        self.doc_folders = os.path.join(self.py_path, doc_folders)
        self.template_dir = os.path.join(self.py_path, template_dir)
        self.variable_dir = os.path.join(self.py_path, variable_dir)
        self.template_base = template_base
        self.base_yml=base_yml
        self.date_fmt = date_fmt
        self.sub_path = ""
        self.sub_filenames = []
        self.md_path = ""
        self.template_sub_dir = ""
        self.check_dir()
    def __str__(self):
        return f"{self.__class__.__name__}{self.str_out}"
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def get_docs(self, docs: list=None):
        # Build absolute path for execution and set output path
        p, directorys, filenames = self.get_files(self.doc_folders)
        #Filter out directories to user specified input if provided
        if not isinstance(docs, (list, set, tuple)):
            raise TypeError("The docs parameter must be a list, set or tuple")
        directorys = docs or directorys
        for directory in directorys:
            dir_path = os.path.join(self.doc_folders, directory)
            if not os.path.exists(dir_path):
                logger.error(f"Folder {dir_path} not found")
                continue
            self.sub_path, sub_directorys, self.sub_filenames = self.get_files(dir_path)
            self.build_context()
            self.render_html()
    
    def check_dir(self):
        os.makedirs(self.result_path, exist_ok=True)
        os.makedirs(self.doc_folders, exist_ok=True)
        os.makedirs(self.template_dir, exist_ok=True)
        os.makedirs(self.variable_dir, exist_ok=True)

    def csv_to_list(self, docs: str) -> list:
        return list(map(str.strip, docs.split(",")))

    def get_files(self, directory):
        return next(os.walk(directory), (None, None, []))

    def make_file_path(self, directory):
        return f'file:{os.path.sep}{os.path.sep}{directory}{os.path.sep}' 
    
    def render_html(self):
        """
        Render html page using jinja based on layout.html
        """
        template_loader = jinja2.FileSystemLoader(searchpath=self.template_sub_dir)
        template_env = jinja2.Environment(loader=template_loader)
        template = template_env.get_template(self.template_base)
        self.set_date()
        output_text = template.render(self.meta_data)
        logger.info(f"Now converting `{self.meta_data['title']}`... ")
        pdf_path = os.path.join(self.result_path, f'{self.meta_data["title"]}.pdf')
        self.html2pdf(output_text, pdf_path)   

    def html2pdf(self, html_string, pdf_path):
        """
        Convert html to pdf using weasyprint which is a wrapper of wkhtmltopdf
        """
        HTML(string=html_string).write_pdf(pdf_path)

    def get_date(self):
        "Get today's date in US format"
        today = date.today()
        return today.strftime(self.date_fmt)

    def set_date(self):
        self.meta_data['date'] = self.meta_data.get('date') or self.get_date()

    def get_yml(self, path_name):
        Loader.vars_path = self.variable_dir
        with open(path_name, "r") as stream:
            try:
                meta_data = yaml.load(stream, Loader)
            except yaml.YAMLError as exc:
                logger.error(exc)
                meta_data = {}
            return meta_data

    def get_abs_path_directory(self, directory):
        path = os.path.dirname(os.path.abspath(directory))
        return path 

    def get_markdown(self) -> str:
        with open(self.md_path, "r") as stream:
            try:
                extensions=['markdown.extensions.extra', 'markdown.extensions.codehilite', 
                            'markdown.extensions.smarty', 'pymdownx.tilde', 'pymdownx.emoji', 
                            'pymdownx.smartsymbols']
                md_html = markdown.markdown(stream.read(), output_format='html',  extensions=extensions)
            except Exception as exc:
                logger.error(f"Unable to render markdown file at {self.md_path}")
                md_html = ""
            return jinja2.Template(md_html)

    def get_sub_sections(self):
        self.meta_data['sections'] = self.meta_data.get('sections', {}) or {}
        new_sub_sections = {}
        for key, val in self.meta_data['sections'].items():
            self.md_path = os.path.join(self.sub_path, val)
            sub_sect_html = self.get_markdown()
            new_sub_sections[key] = sub_sect_html.render(self.meta_data)
        self.meta_data['sections'].update(new_sub_sections)

    def set_meta_data_paths(self):
        self.template_sub_dir = os.path.join(self.template_dir, self.meta_data.get('template', 'report'))
        img_directory = os.path.join(self.sub_path, 'imgs')
        self.meta_data['base_dir'] = self.make_file_path(self.template_sub_dir)
        self.meta_data['img_dir'] = self.make_file_path(img_directory)
        
    def build_context(self):
        if self.base_yml in self.sub_filenames:
            base_file_path = os.path.join(self.sub_path, self.base_yml)
            self.meta_data = self.get_yml(base_file_path)
            self.set_meta_data_paths()
            self.get_sub_sections()
    
    def clean_file_link(self, link: str):
        return link.replace('/', os.sep).replace('\\', os.sep)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Create PDFs for inlcuded docs.')
    parser.add_argument('--doc',  action='append',
        help='Name of the doc folders to generate PDFs', default=[])
    parser.add_argument('--stdout', action='store_true',
        help='Output logs to std out, default None', default=False)
    parser.add_argument('--logging_lvl', choices=logging._nameToLevel.keys(), nargs='?',
        help='Choose Logging Level, Default INFO', default='INFO')
    args = parser.parse_args()
    logging_level = logging._nameToLevel[args.logging_lvl]
    logger.setLevel(logging_level)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler = logging.FileHandler('doc_as_code.log')
    file_handler.setLevel(logging_level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    if args.stdout:
        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.setLevel(logging_level)
        stdout_handler.setFormatter(formatter)
        logger.addHandler(stdout_handler)
    
    myClass = CreatePdfFromDocs(template_base='report.html')
    myClass.get_docs(args.doc)
