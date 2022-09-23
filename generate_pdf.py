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


logger = logging.getLogger()

def get_markdown(path_name) -> str:
    with open(path_name, "r") as stream:
        try:
            extensions=['markdown.extensions.extra', 'markdown.extensions.codehilite', 
                        'markdown.extensions.smarty', 'pymdownx.tilde', 'pymdownx.emoji', 
                        'pymdownx.smartsymbols']
            md_html = markdown.markdown(stream.read(), output_format='html',  extensions=extensions)
        except Exception as exc:
            md_html = ""
        return jinja2.Template(md_html)

def csv_to_list(docs: str) -> list:
    return list(map(str.strip, docs.split(",")))

def check_dir(path):
    os.makedirs(path, exist_ok=True)
    
def render_html(templates_dir, context, template="report.html"):
    """
    Render html page using jinja based on layout.html
    """
    template_loader = jinja2.FileSystemLoader(searchpath=templates_dir)
    template_env = jinja2.Environment(loader=template_loader)
    template = template_env.get_template(template)
    set_date(context)
    output_text = template.render(context)
    logger.info(f"Now converting `{context['title']}`... ")
    pdf_path = os.path.join(result_path, f'{context["title"]}.pdf')
    html2pdf(output_text, pdf_path)   

def html2pdf(html_string, pdf_path):
    """
    Convert html to pdf using weasyprint which is a wrapper of wkhtmltopdf
    """
    HTML(string=html_string).write_pdf(pdf_path)

def get_date():
    "Get today's date in US format"
    today = date.today()
    return today.strftime("%m.%d.%Y")

def set_date(context):
    context['date'] = context.get('date') or get_date()

def get_yml(path_name, variables_folder):
    Loader.vars_path = variables_folder
    with open(path_name, "r") as stream:
        try:
            meta_data = yaml.load(stream, Loader)
        except yaml.YAMLError as exc:
            logger.error(exc)
            meta_data = {}
        return meta_data

def get_abs_path_directory(directory):
    path = os.path.dirname(os.path.abspath(directory))
    return path 

def get_files(directory):
    return next(os.walk(directory), (None, None, []))

def img_to_abs_path(templates_dir, context):
    try:
        context['img'] =  os.path.abspath(os.path.join(templates_dir, context['img']))
    except KeyError as e:
        pass


def get_sub_sections(path, meta_data):
    meta_data['sections'] = meta_data.get('sections', {}) or {}
    new_sub_sections = {}
    for key, val in meta_data['sections'].items():
        sub_section_path = os.path.join(path, val)
        sub_sect_html = get_markdown(sub_section_path)
        new_sub_sections[key] = sub_sect_html.render(meta_data)
    meta_data['sections'].update(new_sub_sections)
    return meta_data

def set_meta_data_paths(meta_data, dir_path):
    templates_dir = os.path.join(py_path, 'templates', meta_data.get('template', 'report'))
    img_directory = os.path.join(dir_path, 'imgs')
    meta_data['base_dir'] = make_file_path(templates_dir)
    meta_data['img_dir'] = make_file_path(img_directory)
    return templates_dir
    
def build_context(path, files, base_yml="meta_data.yml"):
    variables_folder = os.path.join(py_path, 'variables')
    if base_yml in files:
        base_file_path = os.path.join(path, base_yml)
        meta_data = get_yml(base_file_path, variables_folder)
        template_dir = set_meta_data_paths(meta_data, path)
        get_sub_sections(path, meta_data)
    return meta_data, template_dir

def make_file_path(directory):
   return f'file:{os.path.sep}{os.path.sep}{directory}{os.path.sep}' 

def get_docs(docs):
    # Build absolute path for execution and set output path
    setup_path()
    doc_path = os.path.join(py_path, 'docs')
    p, directorys, filenames = get_files(doc_path)
    #Filter out directories to user specified input if provided
    directorys = docs or directorys
    for directory in directorys:
        dir_path = os.path.join(doc_path, directory)
        sub_path, sub_directorys, sub_filenames = get_files(dir_path)
        context, template_dir = build_context(path=sub_path, files=sub_filenames)
        render_html(template_dir, context)

def setup_path(output_dir='results'):
    global py_path, result_path
    py_path = get_abs_path_directory(__file__)
    result_path = os.path.join(py_path, output_dir)
    check_dir(result_path)

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
    

    get_docs(args.doc)
