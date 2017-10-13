# ESLint Rules Scraper

Extracts rules from ESLint's [List of available rules](https://eslint.org/docs/rules/) page.


## Usage

Install Python.

Install the required packages:

````
pip install urllib3
pip install BeautifulSoup4
````

Go to the directory where `eslint-rules-scraper.py` is located.

Run:

````
python eslint-rules-scraper.py
````

`.eslintrc.js`, `.eslintrc.json`, and `.eslintrc.yaml` files (containing ONLY the rules) will be outputted in the same directory where `eslint-rules-scraper.py` is found.

**WARNING**: If you already have files named `.eslintrc.js`, `.eslintrc.json`, or `.eslintrc.yaml` in this directory, they WILL be overwritten.