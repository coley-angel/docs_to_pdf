import jinja2
from weasyprint import HTML, CSS
import os
import yaml
import markdown
from datetime import date



def render_html(templates_dir, context, template="report.html"):
    """
    Render html page using jinja based on layout.html
    """
    template_loader = jinja2.FileSystemLoader(searchpath=templates_dir)
    template_env = jinja2.Environment(loader=template_loader)
    template = template_env.get_template(template)
    output_text = template.render(context)
    css = os.path.join(templates_dir, 'report.css')
    print("Now converting ... ")
    pdf_path = os.path.join(py_path, 'results', f'{context["title"]}.pdf')
    html2pdf(output_text, pdf_path, css)   

def html2pdf(html_string, pdf_path, css):
    """
    Convert html to pdf using weasyprint which is a wrapper of wkhtmltopdf
    """
    HTML(string=html_string).write_pdf(pdf_path, stylesheets=[CSS(css)])

def get_date():
    "Get today's date in US format"
    today = date.today()
    return today.strftime("%m.%d.%Y")

def get_yml(path_name):
    with open(path_name, "r") as stream:
        try:
            meta_data = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            meta_data = {}
        return meta_data

def get_markdown(path_name) -> str:
    with open(path_name, "r") as stream:
        try:
            md_html = markdown.markdown(stream.read(), output_format='html',  extensions=['markdown.extensions.extra'])
        except Exception as exc:
            md_html = ""
        return md_html

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

# def get_sub_sections(path, meta_data, templates_dir):
#     for key, val in meta_data.get('sections', {}).items():
#         sub_section_path = os.path.join(path, val)
#         sub_sect_dict = get_yml(sub_section_path)
#         img_to_abs_path(templates_dir, sub_sect_dict)
#         meta_data['sections'][key] = sub_sect_dict
#     return meta_data

def get_sub_sections(path, meta_data, templates_dir):
    for key, val in meta_data.get('sections', {}).items():
        sub_section_path = os.path.join(path, val)
        sub_sect_html = get_markdown(sub_section_path)
        print(sub_sect_html)
        meta_data['sections'][key] = sub_sect_html
    return meta_data

    
def build_context(path, files, templates_dir, base_yml="meta_data.yml"):
    if base_yml in files:
        base_file_path = os.path.join(path, base_yml)
        meta_data = get_yml(base_file_path)
        img_to_abs_path(templates_dir, meta_data)      
        get_sub_sections(path, meta_data, templates_dir)
    return meta_data

def get_docs(py_path):
    doc_path = os.path.join(py_path, 'docs')
    p, directorys, filenames = get_files(doc_path)
    for directory in directorys:
        dir_path = os.path.join(doc_path, directory)
        sub_path, sub_directorys, sub_filenames = get_files(dir_path)
        templates_dir = os.path.join(py_path, 'templates', 'report')
        context = build_context(path=sub_path, files=sub_filenames, templates_dir=templates_dir)
        render_html(templates_dir, context)

if __name__ == "__main__":
    global py_path
    py_path = get_abs_path_directory(__file__)
    get_docs(py_path)
