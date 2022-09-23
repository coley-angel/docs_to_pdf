import yaml
import os
import logging
logger = logging.getLogger('yaml loader')
import markdown
import jinja2

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
    
class Loader(yaml.SafeLoader): 
    vars_path = ""
    def __init__(self, stream):
        self.docs_path = os.path.split(stream.name)[0]
        super().__init__(stream)
    
    def md_template(self, md_filename):
        filename = os.path.join(self.docs_path, self.construct_scalar(md_filename))
        try:
            with open(filename, 'r') as f:
                return get_markdown(filename).render()
        except FileNotFoundError:
            logger.error(f"No file found for {filename} in folder {self._docs_path}")

    def include(self, node):
        filename = os.path.join(self.vars_path, self.construct_scalar(node))
        try:
            with open(filename, 'r') as f:
                return yaml.load(f, Loader)
        except FileNotFoundError:
            logger.error(f"No file found for {filename} in folder {self.vars_path}")

Loader.add_constructor('!include', Loader.include)
Loader.add_constructor('!md_template', Loader.md_template)