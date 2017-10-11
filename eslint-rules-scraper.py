import requests
from bs4 import BeautifulSoup

page = requests.get("https://eslint.org/docs/rules/")
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

	table = header.find_next_sibling("table")

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

