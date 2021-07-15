import os
import json
import sys
import csv
import requests
import time

projectPath = os.path.normpath(os.getcwd() + os.sep + os.pardir)
sys.path.append(projectPath)

class codeforces():
    def __init__(self):
        self.finalData = dict()
        self.finalData["source"] = "https://codeforces.com/api/user.ratedList"
        self.finalData["description"] = "codeforces.com user profile data"
        self.finalData["creation time"] = int(time.time())
        self.finalData['organization'] = dict()
        self.url = "https://codeforces.com/api/user.ratedList"
        self.rawData = dict()


    def getData(self):
        data = requests.get(self.url, stream=True)
        print(f"requests status code {data.status_code}\n")

        loaded = 0

        with open('rawData.json', 'wb') as rawData:
            for chunk in data.iter_content(chunk_size=1024):
                loaded += 1
                if chunk:
                    rawData.write(chunk)
                os.system('clear')
                print(loaded, "mb data loaded in rawData.json")
        print("\nAll data saved in rawData.json successfully!!")

    def processData(self):
        try:
            with open('rawData.json', 'r') as f:
                self.rawData = json.load(f)
            print("\nrawData.json loaded!!\n")
        except Exception as e:
            print('rawData json loading exception:', e)
            return

        print("---------------------------")
        print("rawData keys:")
        print("---------------------------")
        for i in self.rawData:
            print(i)
        print("---------------------------")
        print("'result' is the list of user profile data:")
        print("total profile data available is:", len(self.rawData['result']))
        print("---------------------------")
        print("First profile sample:")
        print("---------------------------")
        print(json.dumps(self.rawData['result'][0], indent=2))
        print("---------------------------")

        for i in self.rawData['result']:
            if 'organization' in i and 'country' in i:
                organization = ' '.join([x.strip() for x in i['organization'].strip().split() if x.strip() != ''])
                country = ' '.join([x.strip() for x in i['country'].strip().split() if x.strip() != ''])
                city = country
                if 'city' in i:
                    c = ' '.join([x.strip() for x in i['city'].strip().split() if x.strip() != ''])
                    if c != '':
                        city = c + ', ' + city

                d = dict()
                d['name'] = organization
                d['address'] = city
                d['country'] = country

                tmp = organization.split()

                if len(tmp) > 1 and organization != '' and country != '':
                    self.finalData['organization'][d['name'].lower()] = d
        print("\nData processing done.")

    def saveData(self):
        with open('finalData.json', 'w') as f:
            json.dump(self.finalData, f, indent=2)
        print("\nself.finalData saved in finalData.json successfully!!")
        print("\ntotal data:", len(self.finalData['organization']))


def main():
    cf = codeforces()
    # it will load a 150+ mb json file
    # uncomment it when need to load rawData.json
    # cf.getData()
    cf.processData()
    cf.saveData()

if __name__ == '__main__':
    main()
