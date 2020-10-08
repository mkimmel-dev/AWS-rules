import boto3
import json
from bs4 import BeautifulSoup as bsoup
import requests
import re

rules = []
ruledata = []
identifiers = []
def rule_collect():
    global rules
    global ruledata
    global identifiers
#gathering list of rule names
    page = requests.get("https://docs.aws.amazon.com/config/latest/developerguide/managed-rules-by-aws-config.html")
    soup = bsoup(page.text, 'html.parser')



#stripping out the rule names and formatting for URL
    for i in soup.find_all('li'):
        rules.append(str(i.text))

#going to the doc page for each rule
    identifytemplateurl = "https://docs.aws.amazon.com/config/latest/developerguide/"
    ruleidentifyurl = [identifytemplateurl + i  + ".html" for i in rules]

#stripping out just the identifier tag from the html
    for i in range(len(ruleidentifyurl)):
        identifypage = requests.get(ruleidentifyurl[i])
        identifysoup = bsoup(identifypage.text,'html.parser')
        pidentify = identifysoup.find_all('p')
#finding where the identifier is
        start = str(pidentify).find("Identifier:</b>") + len("Identifier:</b>")
        end = str(pidentify).find("</p>") + start
        substring = str(pidentify)[start:end]
#stripping out the extra bits
        subend = substring.find("</p>")
        subsub = substring[:subend]
        identifiers.append(subsub.strip())

#cleaning it up for use in further URL
#    identifiers = [s.strip() for s in identifiers]
    print(*identifiers, sep='\n')
#generating URLs for ruledata
    datatemplateurl = "https://s3.amazonaws.com/aws-configservice-us-east-1/cloudformation-templates-for-managed-rules/"
    ruledataurl = [datatemplateurl + i + ".template" for i in identifiers]

#gathering info
    for i in range(len(ruledataurl)):
        rulepage = requests.get(ruledataurl[i])
        rulesoup = bsoup(rulepage.text, 'html.parser')
        ruledata.append(str(rulesoup))

#formatting to JSON
    ruledata = [data + "," for data in ruledata]
    ruledata.insert(0,"[").append("]")


if __name__ == '__main__':
    rule_collect()
#writing to file
    with open('config_rules.txt','w') as outfile:
        outfile.writelines("%s\n" % data for data in ruledata)


