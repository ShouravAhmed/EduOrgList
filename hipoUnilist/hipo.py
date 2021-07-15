import requests
import json
import time

import os
projectPath = os.path.normpath(os.getcwd() + os.sep + os.pardir)

class hipoUniDomainList():
    def __init__(self):
        self.finalData = dict()
        self.finalData["source"] = "https://github.com/Hipo/university-domains-list"
        self.finalData["description"] = "JSON file that contains domains, names and countries of most of the universities of the world."
        self.finalData["creation time"] = int(time.time())
        self.finalData['organization'] = dict()

    def getData(self):
        response = requests.get('https://raw.githubusercontent.com/Hipo/university-domains-list/master/world_universities_and_domains.json')
        jsonData = response.json()

        for uni in jsonData:
            d = dict()
            d['name'] = ' '.join([x.strip() for x in uni["name"].split() if x.strip() != ''])
            if len(uni["web_pages"]) > 0:
                d['website'] = uni["web_pages"][0]
            d["country"] = uni["country"]

            self.finalData['organization'][d['name'].lower()] = d

    def saveData(self):
        with open('finalData.json', 'w') as f:
            json.dump(self.finalData, f, indent=2)
        print("Total", len(self.finalData['organization']), "data saved in finalData.json")



def main():
    code = hipoUniDomainList()
    code.getData()
    code.saveData()

if __name__ == '__main__':
    main()
