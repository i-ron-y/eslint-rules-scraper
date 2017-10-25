# ESLint Rules Scraper

Extracts rules from ESLint's [List of available rules](https://eslint.org/docs/rules/) page.


## Usage

Install Python.

Install the required packages:

````
pip install urllib3
pip install requests
pip install BeautifulSoup4
````

Go to the directory where `eslint-rules-scraper.py` is located.

Run:

````
python eslint-rules-scraper.py [filetype [filename]]
````

Valid filetypes are: `js`, `json`, `yaml`


Output for 0 arguments:

`.eslintrc.js`, `.eslintrc.json`, and `.eslintrc.yaml` files (containing ONLY the rules) will be outputted in the same directory where `eslint-rules-scraper.py` is found.

Output for 1 argument:

A `.eslintrc` file (containing ONLY the rules) in `js`, `json`, or `yaml` format, according to user input, will be outputted in the same directory where `eslint-rules-scraper.py` is found.

Output for 2 arguments:

A file (containing ONLY the rules) in `js`, `json`, or `yaml` format, according to user input, will be outputted in the same directory where `eslint-rules-scraper.py` is found.


**WARNING**: If you already have files of the same name as the respective output files in this directory, they WILL be overwritten.