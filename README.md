# Create PDF documents using markdown, html templates and python

## Ubuntu 20.4 dependencies for weasyprint python lib
### Install
1. apt install python3-pip libpango-1.0-0 libharfbuzz0b libpangoft2-1.0-0 fonts-open-sans
1. run `pip install -r requirements.txt`
   
## Basic Use case -> generate styalized pdf's using html templates
1. Install python (see above for ubuntu instructions)
2. Install git (should be included, check `git -v`)
3. Clone repository `git clone *url*`
4. Create document folder under docs folder
5. add meta_data.yml file under previously created folder
6. add a sections key to the meta_data.yaml file
   1. For every markdown file you want to include add a key under sections
   2. The key should be the name and the value the filename **in the same directory**