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
	rulesAll = []

	rulesSoup = table.find_all('p')

	for r in rulesSoup:
		rulesAll.append(r.get_text())
	
	# e.g. [(RuleName1, RuleDef1), (RuleName2, RuleDef2), ...]
	rules = list(zip(rulesAll[0::2], rulesAll[1::2]))

	# e.g. (RuleType1, [(RuleName1, RuleDef1), (RuleName2, RuleDef2), ...])
	ruleGroup = (types[i], rules)

	ruleGroups.append(ruleGroup)


# Here is where the .eslintrc.js, .eslintrc.json, and .eslintrc.yaml files (containing ONLY the rules) are outputted,
# in the same directory where eslint-rules-scraper.py is found.
# 
# WARNING: If you already have files named .eslintrc.js, .eslintrc.json, or .eslintrc.yaml in this directory, they WILL be overwritten.

def outputRules(type):

	linebreak = '\n'*2
	indent = ' '*4
	outputString = ''

	if type == 'yaml':
		usageStringLineStart = indent + '#'
		commentHeader = '#'*8
		headerIndent = indent
		commentDefn = '# '
		columnDefn = 41
		usageStringExample = 'quotes: [2, double]'

	if type == 'json':
		usageStringLineStart = indent*2 + '//'
		commentHeader = '/'*8
		headerIndent = indent*2
		commentDefn = '// '
		columnDefn = 48
		usageStringExample = '"quotes": [2, "double"]'

	usageString = (usageStringLineStart + ' Usage:\n' +
				   usageStringLineStart + indent + '"off" or 0 - turn the rule off\n' +
				   usageStringLineStart + indent + '"warn" or 1 - turn the rule on as a warning (doesn’t affect exit code)\n' +
				   usageStringLineStart + indent + '"error" or 2 - turn the rule on as an error (exit code is 1 when triggered)\n' +
				   usageStringLineStart + '\n' +
				   usageStringLineStart + indent + 'If a rule has additional options, you can specify them using array literal syntax, such as:\n' +
				   usageStringLineStart + indent*2 + usageStringExample + '\n')

	if type == 'yaml':
		outputString = 'rules:' + linebreak + usageString + linebreak
		ruleNameStart = indent
		ruleNameEnd = ': 0'

	if type == 'json':
		outputString = '{' + linebreak + indent + '"rules": {' + linebreak + usageString + linebreak
		ruleNameStart = indent*2 + '"'
		ruleNameEnd = '": 0,'

	for rg in range(len(ruleGroups)):
		headerString = headerIndent + commentHeader + ' ' + ruleGroups[rg][0] + ' ' + commentHeader

		groupRulesString = ''

		for rn in range(len(ruleGroups[rg][1])):
			ruleNameString = ruleNameStart + ruleGroups[rg][1][rn][0] + ruleNameEnd
			ruleDefnString = commentDefn + ruleGroups[rg][1][rn][1]
			ruleString = ruleNameString + ' '*(columnDefn-len(ruleNameString)) + ruleDefnString
			groupRulesString += ruleString + '\n'

		groupString = headerString + linebreak + groupRulesString

		outputString += groupString + linebreak

	if type == 'json':
		outputString += indent + '}' + linebreak + '}'

	return outputString


jsonOutputString = outputRules('json')
jsOutputString = 'module.exports = ' + jsonOutputString
yamlOutputString = outputRules('yaml')


f = open('.eslintrc.json', 'w')
f.write(jsonOutputString)
f.close()

f = open('.eslintrc.js', 'w')
f.write(jsOutputString)
f.close()

f = open('.eslintrc.yaml', 'w')
f.write(yamlOutputString)
f.close()