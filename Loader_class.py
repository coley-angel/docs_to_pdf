import yaml
import os

class Loader(yaml.SafeLoader):


    def include(self, node):
        filename = os.path.join(self._root, self.construct_scalar(node))
        try:
            with open(filename, 'r') as f:
                return yaml.load(f, Loader)
        except FileNotFoundError:
            print(f"No file found for {filename} in folder {self._root}")

Loader.add_constructor('!include', Loader.include)