import os
import json
import sys
import csv

projectPath = os.path.normpath(os.getcwd() + os.sep + os.pardir)
sys.path.append(projectPath)

import ots

import threading
from concurrent.futures import ThreadPoolExecutor


uniData = dict()

class allUniversityData(ots.one_time_scraper):
    def __init__(self):
        super().__init__()
        self.url = "https://www.4icu.org/reviews/index"

    def getData(self, pageNo):
        self.url = self.url + str(pageNo) + ".htm"
        self.fetch(self.url)

        unis = self.bts.find('table')
        unis = unis.find_all('tr')

        for uni in unis:
            try:
                td = uni.find_all('td')
                if(len(td) == 2):
                    organization = td[0].find('a').text.strip()
                    organization = organization.split()
                    organization = ' '.join(organization)

                    try:
                        country = td[1].find('img')
                        country = country.attrs['alt']
                    except:
                        country = ""

                    uniData[organization] = country
            except:
                pass

def saveData():
    results = list()
    for (x, y) in uniData.items():
        d = dict()
        d['organization'] = x
        d['country'] = y
        results.append(d)

    with open('res.csv', 'w') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=results[0].keys())
        writer.writeheader()
        for row in results:
            writer.writerow(row)
    print("\nAll data written in 'res.csv' successfully.")


def saveFinalData():
    finalResult = list()
    finalData = {}

    try:
        with open(projectPath+"/educationalInstituteData.csv", 'r') as csv_file:
            reader = csv.DictReader(csv_file)

            for row in reader:
                d = dict(row)
                finalData[d['organization']] = d['country']
    except:
        pass

    for (x, y) in uniData.items():
        finalData[x] = y

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
    with ThreadPoolExecutor(max_workers=10) as executor:
        for i in range(2, 28):
            uni = allUniversityData()
            executor.submit(uni.getData, i)

    saveData()
    saveFinalData()


if __name__ == '__main__':
    main()
