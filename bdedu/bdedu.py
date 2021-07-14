import openpyxl

import json
import csv

import os
projectPath = os.path.normpath(os.getcwd() + os.sep + os.pardir)

import threading
from concurrent.futures import ThreadPoolExecutor


class bdEduDataCollector():
    # data source
    # https://banbeis.portal.gov.bd/

    def __init__(self):
        self.allData = list()
        self.shortData = list()

    def readSchool(self):
        # data source
        # http://banbeis.portal.gov.bd/sites/default/files/files/banbeis.portal.gov.bd/npfblock/school.xlsx

        sheets = openpyxl.load_workbook('school.xlsx')
        sheet = sheets['Sheet1']
        rows = sheet.rows

        header = [cell.value for cell in next(rows)]

        for row in rows:
            rowData = [cell.value for cell in row]
            school = dict()
            for i in range(len(rowData)):
                school[header[i]] = rowData[i]

            self.allData.append(school)

        print("\nschool data fatched!")

    def readCollege(self):
        # data source
        # http://banbeis.portal.gov.bd/sites/default/files/files/banbeis.portal.gov.bd/npfblock/college.xlsx

        sheets = openpyxl.load_workbook('college.xlsx')
        sheet = sheets['Sheet1']
        rows = sheet.rows

        header = [cell.value for cell in next(rows)]

        for row in rows:
            rowData = [cell.value for cell in row]
            college = dict()
            for i in range(len(rowData)):
                college[header[i]] = rowData[i]

            self.allData.append(college)

        print("\ncollege data fatched!")


    def readMadrasa(self):
        # data source
        # http://banbeis.portal.gov.bd/sites/default/files/files/banbeis.portal.gov.bd/npfblock/madrasa.xlsx

        sheets = openpyxl.load_workbook('madrasa.xlsx')
        sheet = sheets['Sheet1']
        rows = sheet.rows

        header = [cell.value for cell in next(rows)]

        for row in rows:
            rowData = [cell.value for cell in row]
            madrasa = dict()
            for i in range(len(rowData)):
                madrasa[header[i]] = rowData[i]

            self.allData.append(madrasa)

        print("\nmadrasa data fatched!")


    def readSchoolCollege(self):
        # data source
        # http://banbeis.portal.gov.bd/sites/default/files/files/banbeis.portal.gov.bd/npfblock/School%26college.xlsx

        sheets = openpyxl.load_workbook('schoolcollege.xlsx')
        sheet = sheets['Sheet1']
        rows = sheet.rows

        header = [cell.value for cell in next(rows)]

        for row in rows:
            rowData = [cell.value for cell in row]
            schoolCollege = dict()
            for i in range(len(rowData)):
                schoolCollege[header[i]] = rowData[i]

            self.allData.append(schoolCollege)

        print("\nschool and college data fatched!")

    def processData(self):
        for i in range(len(self.allData)):
            for j in self.allData[i]:
                try:
                    d = self.allData[i][j]
                    d = d.replace(',' , ' | ')
                    d = d.strip()
                    d = d.split()
                    d = ' '.join(d)
                    self.allData[i][j] = d
                except:
                    pass


    def to_csv_originalData(self):
        with open('originalData.csv', 'w') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self.allData[0].keys())
            writer.writeheader()
            for row in self.allData:
                writer.writerow(row)
        print("\nAll Original data written in 'originalData.csv' successfully.")

    def to_csv_processedData(self):
        for inst in self.allData:
            d = dict()
            d["organization"] = str(inst["INSTITUTE_NAME"])
            d["country"] = "Bangladesh"
            self.shortData.append(d)

        print("\nTotal", len(self.shortData), " bdEdu Inistitute data loaded.")

        with open('res.csv', 'w') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self.shortData[0].keys())
            writer.writeheader()
            for row in self.shortData:
                writer.writerow(row)
        print("\nAll data written in 'res.csv' successfully.")


    def saveFinalData(self):
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
    bdedu = bdEduDataCollector()

    with ThreadPoolExecutor(max_workers=4) as executor:
        executor.submit(bdedu.readCollege())
        executor.submit(bdedu.readSchool())
        executor.submit(bdedu.readSchoolCollege())
        executor.submit(bdedu.readMadrasa())

    bdedu.processData()

    bdedu.to_csv_originalData()
    bdedu.to_csv_processedData()

    bdedu.saveFinalData()

    # https://banbeis.portal.gov.bd/sites/default/files/files/banbeis.portal.gov.bd/npfblock/Private%20University.xls
    # https://banbeis.portal.gov.bd/sites/default/files/files/banbeis.portal.gov.bd/npfblock//Public%20University%202019.xls


if __name__ == '__main__':
    main()
