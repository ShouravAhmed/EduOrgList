import requests
import json
import csv

import os
projectPath = os.path.normpath(os.getcwd() + os.sep + os.pardir)

class codeOrgPublicSchoolData():
    def __init__(self):
        self.originalData = list()
        self.shortData = list()

    def getData(self):
        response = requests.get('https://code.org/schools.json')
        jsonData = response.json()
        schools = jsonData['schools']

        for school in schools:
            d = dict()
            for (x, y) in school.items():
                val = y
                if type(val) == type([]):
                    val = ' | '.join(val)
                val = str(val)
                val = val.strip()
                val = val.split()
                val = ' '.join(val)
                d[x] = val
            self.originalData.append(d)

    def saveOriginalData(self):
        with open('originalData.csv', 'w') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self.originalData[0].keys())
            writer.writeheader()
            for row in self.originalData:
                writer.writerow(row)
        print("\nAll Original data written in 'originalData.csv' successfully.")

    def saveShortData(self):
        for school in self.originalData:
            d = dict()
            d["organization"] = str(school['name'])
            d["country"] = str(school['country'])
            self.shortData.append(d)

        print("\nTotal", len(self.shortData), " Inistitute data loaded from [code.org].")

        with open('res.csv', 'w') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self.shortData[0].keys())
            writer.writeheader()
            for row in self.shortData:
                writer.writerow(row)
        print("\nAll data written in 'res.csv' successfully.")


    def saveFinalData(self):
        finalResult = list()
        finalData = dict()

        try:
            with open(projectPath+"/educationalInstituteData.csv", 'r') as csv_file:
                reader = csv.DictReader(csv_file)

                for row in reader:
                    d = dict(row)
                    finalData[d['organization']] = d['country']
        except:
            pass

        for d in self.shortData:
            finalData[d['organization']] = d['country']

        for (organization, country) in finalData.items():
            d = {
                'organization' : organization,
                'country' : country
            }
            finalResult.append(d)

        with open(projectPath+"/educationalInstituteData.csv", 'w') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=finalResult[0].keys())
            writer.writeheader()
            for row in finalResult:
                writer.writerow(row)

        print("\nFinal data written in 'EduOrgList/educationalInstituteData.csv' successfully.")
        print("Final dataset size:", len(finalResult))


def main():
    code = codeOrgPublicSchoolData()
    code.getData()
    code.saveOriginalData()
    code.saveShortData()
    code.saveFinalData()



if __name__ == '__main__':
    main()
