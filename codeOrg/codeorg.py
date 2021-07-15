import requests
import json
import csv
import time

import os
projectPath = os.path.normpath(os.getcwd() + os.sep + os.pardir)

class codeOrgPublicSchoolData():
    def __init__(self):
        self.finalData = dict()
        self.finalData["source"] = "https://code.org/schools.json"
        self.finalData["description"] = "Code.org local school search database"
        self.finalData["creation time"] = int(time.time())
        self.finalData['organization'] = dict()

    def getData(self):
        response = requests.get('https://code.org/schools.json')
        jsonData = response.json()
        schools = jsonData['schools']

        for school in schools:
            tmp = dict()
            d = dict()
            for (x, y) in school.items():
                val = y
                if type(val) == type([]):
                    val = ' | '.join(val)
                val = str(val)
                val = val.strip()
                val = val.split()
                val = ' '.join(val)
                tmp[x] = val
            d['name'] = tmp["name"]
            d['website'] = tmp["website"]
            d['tel'] = tmp["contact_number"]
            d['email'] = tmp["contact_email"]
            d["student enrollment"] = tmp["number_of_students"]
            d["gender"] = tmp["gender"]
            address = ""
            if tmp["street"] != None:
                address = address + tmp["street"]
            if tmp["city"] != None:
                address = address + tmp["city"]
            if tmp["state"] != None:
                address = address + tmp["state"]
            if tmp["zip"] != None:
                address = address + tmp["zip"]
            d["address"] = address
            d["country"] = tmp["country"]

            self.finalData['organization'][d['name'].lower()] = d

def main():
    code = codeOrgPublicSchoolData()
    code.getData()
    with open('finalData.json', 'w') as f:
        json.dump(code.finalData, f, indent=2)
    print("Total", len(code.finalData['organization']), "data saved in finalData.json")

if __name__ == '__main__':
    main()
