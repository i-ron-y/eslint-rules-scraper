# ESLint Rules Scraper

Extracts rules from ESLint's [List of available rules](https://eslint.org/docs/rules/) page and outputs ESLint config files containing ONLY the rules, set to 0.


## Usage

Install Python.

Install the required packages:

````
pip install requests
pip install BeautifulSoup4
````

Go to the directory where `eslint-rules-scraper.py` is located.

Run:

````
python eslint-rules-scraper.py [filetype [filename]]
````

Valid filetypes are: `js`, `json`, `yaml`
<br />
<br />
##### Output for 0 arguments:

`.eslintrc.js`, `.eslintrc.json`, and `.eslintrc.yaml` files (containing ONLY the rules, set to 0) will be outputted in the same directory where `eslint-rules-scraper.py` is found.
<br />
<br />
##### Output for 1 argument:

A `.eslintrc` file (containing ONLY the rules, set to 0) in `js`, `json`, or `yaml` format, according to user input, will be outputted in the same directory where `eslint-rules-scraper.py` is found.
<br />
<br />
##### Output for 2 arguments:

A file with a user-provided name (containing ONLY the rules, set to 0) in `js`, `json`, or `yaml` format, according to user input, will be outputted in the same directory where `eslint-rules-scraper.py` is found.
<br />
<br />
<br />
**WARNING**: If you already have files of the same name as the respective output files in this directory, they WILL be overwritten.