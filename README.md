# Create PDF documents using markdown, html templates and python


## Ubuntu 20.4 dependencies for weasyprint python lib
### Install
1. apt install python3-pip libpango-1.0-0 libharfbuzz0b libpangoft2-1.0-0 fonts-open-sans
1. run `pip install -r requirements.txt`

## MAC OS dependencies
### Install
1. Install [homebrew](https://brew.sh/ "Homebrew")
1. brew install python pango libffi
   
## Basic Use case -> generate styalized pdf's using html templates
1. Install python (see above for ubuntu instructions)
2. Install git (should be included, check `git -v`)
3. Clone repository `git clone *url*`
4. Create document folder under docs folder
5. add meta_data.yml file under previously created folder
6. add a sections key to the meta_data.yaml file
   1. For every markdown file you want to include add a key under sections
   2. The key should be the name and the value the filename **in the same directory**
   3. Have fun with it or dont

## Running the script
1. windows `python generate_pdf_class.py`
2. linux/mac `python3 generate_pdf_class.py`

## view flags:
1. windows `python generate_pdf_class.py --help`
2. linux/mac `python3 generate_pdf_class.py --help`

| flag | Org | type |
| ------ | ----------- | ----- |
| --stdout   | view logs in stdout | bool |
| --logging_lvl  | Choose Logging Level, Default INFO | str example: --logging_lvl DEBUG |
| --doc | Name of the doc folders to generate PDFs | str example: --doc "my doc folder name"|
