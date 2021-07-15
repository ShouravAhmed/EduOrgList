import requests
import json
import time

import os
projectPath = os.path.normpath(os.getcwd() + os.sep + os.pardir)

class hipoUniDomainList():
    def __init__(self):
        self.finalData = dict()
        self.finalData["source"] = "https://github.com/MLH/mlh-policies/blob/master/schools.csv"
        self.finalData["description"] = "List of schools name only"
        self.finalData["creation time"] = int(time.time())
        self.finalData['organization'] = dict()

    def getData(self):
        response = requests.get('https://raw.githubusercontent.com/MLH/mlh-policies/master/schools.csv')
        schoolList = response.text.split('\n')[1:]
        for school in schoolList:
            name = ' '.join([x.strip() for x in school.split() if x.strip() != ''])
            if len(name):
                if name[0] == '"':
                    name = name[1:]
            if len(name):
                if name[-1] == '"':
                    name = name[:-1]
            self.finalData['organization'][name.lower()] = {'name':name}

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
