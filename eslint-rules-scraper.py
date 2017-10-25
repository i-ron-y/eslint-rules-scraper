import sys
import requests
from bs4 import BeautifulSoup

# Here is where the data scraping happens.

page = requests.get('https://eslint.org/docs/rules/')
soup = BeautifulSoup(page.content, 'html.parser')


# e.g. ['possible-errors', ...]
typeIds = []

# e.g. ['Possible Errors', ...]
types = []

for tag in soup.find_all('h2',{'id':True}):
	if not (tag['id'] == 'deprecated' or tag['id'] == 'removed'):
		typeIds.append(tag['id'])
		types.append(tag.get_text())


# e.g. [(RuleType1, [(RuleName1, RuleDef1), (RuleName2, RuleDef2), ...]), (RuleType2, [...]), ...]
ruleGroups = []

for i in range(len(typeIds)):
	header = soup.find(id=typeIds[i])

	table = header.find_next_sibling('table')

	# e.g. [RuleName1, RuleDef1, RuleName2, RuleDef2, ...]
	tableContents = []

	tableSoup = table.find_all('p')

	for item in tableSoup:
		tableContents.append(item.get_text())
	
	# e.g. [(RuleName1, RuleDef1), (RuleName2, RuleDef2), ...]
	rules = list(zip(tableContents[0::2], tableContents[1::2]))

	# e.g. (RuleType1, [(RuleName1, RuleDef1), (RuleName2, RuleDef2), ...])
	ruleGroup = (types[i], rules)

	ruleGroups.append(ruleGroup)


# Here is where the .eslintrc.js, .eslintrc.json, and .eslintrc.yaml files (containing ONLY the rules) are outputted,
# in the same directory where eslint-rules-scraper.py is found.
# 
# WARNING: If you already have files named .eslintrc.js, .eslintrc.json, or .eslintrc.yaml in this directory, they WILL be overwritten.

indent = ' '*4
linebreak = '\n'*2

firstIndent = ''
secondIndent = ''


# Helper function: Prepare the usage instruction comment string
def prepareUsageString(type):

	# if type == 'js' or type == 'json'
	usageStringLineStart = secondIndent + '//'
	usageStringExample = '"quotes": [2, "double"]'
	
	if type == 'yaml':
		usageStringLineStart = secondIndent + '#'
		usageStringExample = 'quotes: [2, double]'

	usageString = (usageStringLineStart + ' Usage:\n' +
				   usageStringLineStart + indent + '"off" or 0 - turn the rule off\n' +
				   usageStringLineStart + indent + '"warn" or 1 - turn the rule on as a warning (doesn’t affect exit code)\n' +
				   usageStringLineStart + indent + '"error" or 2 - turn the rule on as an error (exit code is 1 when triggered)\n' +
				   usageStringLineStart + '\n' +
				   usageStringLineStart + indent + 'If a rule has additional options, you can specify them using array literal syntax, such as:\n' +
				   usageStringLineStart + indent*2 + usageStringExample + '\n')

	return usageString


# Helper function: Format the rules and rule groups
def formatRules(type):

	formattedRules = ''

	commentSymbol = '//'
	columnDefn = 48
	ruleNameStart = secondIndent
	ruleNameEnd = ': 0'
	commentHeader = commentSymbol*4

	if (type == 'js') or (type == 'json'):
		ruleNameStart += '"'
		ruleNameEnd = '": 0,'

	if type == 'yaml':
		commentSymbol = '#'
		columnDefn = 41
		commentHeader = commentSymbol*8

	for rg in range(len(ruleGroups)):

		headerString = secondIndent + commentHeader + ' ' + ruleGroups[rg][0] + ' ' + commentHeader

		groupRulesString = ''

		for rn in range(len(ruleGroups[rg][1])):
			
			if ((type == 'js') or (type == 'json')) and (rg == len(ruleGroups)-1) and (rn == len(ruleGroups[rg][1])-1):
				ruleNameEnd = '": 0'

			ruleNameString = ruleNameStart + ruleGroups[rg][1][rn][0] + ruleNameEnd
			ruleDefnString = commentSymbol + ' ' + ruleGroups[rg][1][rn][1]
			ruleString = ruleNameString + ' '*(columnDefn-len(ruleNameString)) + ruleDefnString
			groupRulesString += ruleString + '\n'

		groupString = headerString + linebreak + groupRulesString

		formattedRules += groupString + linebreak

	return formattedRules


# Helper function: Format the output file
def formatOutput(type):

	global firstIndent
	global secondIndent

	firstIndent = indent

	ruleConfigHeader = '"rules": {'

	if type == 'yaml':
		firstIndent = ''
		ruleConfigHeader = 'rules:'

	secondIndent = firstIndent + indent

	outputStart = firstIndent + ruleConfigHeader

	if type == 'json':
		outputStart = '{' + linebreak + outputStart

	if type == 'js':
		outputStart = 'module.exports = {' + linebreak + outputStart

	usageString = prepareUsageString(type)

	formattedRules = formatRules(type)
	
	outputEnd = ''

	if (type == 'js') or (type == 'json'):
		outputEnd = firstIndent + '}' + linebreak + '}'

	outputString = outputStart + linebreak + usageString + linebreak + formattedRules + outputEnd

	return outputString


# Output the file(s)

filetypes = ['js', 'json', 'yaml']

# No arguments: Output .eslintrc.js, .eslintrc.json, and .eslintrc.yaml
if len(sys.argv) == 1:

	for ft in filetypes:
		filename = '.eslintrc.' + ft
		
		f = open(filename, 'w')
		f.write(formatOutput(ft))
		f.close()

# 1 argument: Output .eslintrc file in either js, json, or yaml format, according to user input
elif len(sys.argv) == 2:

	if sys.argv[1] not in filetypes:

		print('Valid filetypes are: js, json, yaml\n')

	else:

		filename = '.eslintrc.' + sys.argv[1]

		f = open(filename, 'w')
		f.write(formatOutput(sys.argv[1]))
		f.close()

# 2 arguments: Output a file in either js, json, or yaml format (user inputs filetype and filename)
elif len(sys.argv) == 3:

	if sys.argv[1] not in filetypes:

		print('Valid filetypes are: js, json, yaml\n')

	else:

		filename = sys.argv[2] + '.' + sys.argv[1]

		f = open(filename, 'w')
		f.write(formatOutput(sys.argv[1]))
		f.close()	

else:

	print('Usage: python eslint-rules-scraper.py [filetype [filename]]\n')
	print('Valid filetypes are: js, json, yaml\n')
	print('Please input filename without extension - extension is automatically the selected filetype.')

