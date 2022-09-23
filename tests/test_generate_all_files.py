import pytest
import os
import generate_pdf_class

# Instatiate file paths and class
test_dir = os.path.dirname(os.path.abspath(__file__))
main_path =  os.path.abspath(os.path.join(test_dir, os.pardir))
test_result = 'results'
docs_folder = 'docs'
test_result_path = os.path.join(test_dir, test_result)
doc_folders = os.path.join(main_path, docs_folder)
myClass = generate_pdf_class.CreatePdfFromDocs(template_base='report.html', output_dir=test_result_path)

class TestClass:
    p, directorys, filenames = next(os.walk(doc_folders), (None, None, []))
    @pytest.mark.parametrize("directory", directorys)
    def test_gen_each_doc(self, directory):
        # Create test for each folder in the docs directory
        myClass.get_docs([directory])

    def test_gen_all(self):
        myClass.get_docs([])
