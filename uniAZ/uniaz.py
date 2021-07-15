import os
import json
import sys
import csv
import time

projectPath = os.path.normpath(os.getcwd() + os.sep + os.pardir)
sys.path.append(projectPath)

import ots

import threading
from concurrent.futures import ThreadPoolExecutor


urlList = dict()
finalData = dict()

totalProcessed = 0
processLap = 0

class allUniversityData(ots.one_time_scraper):
    def __init__(self):
        super().__init__()
        self.url = ""
        finalData['source'] = "https://www.4icu.org/";
        finalData['description'] = 'Detaild information of all Universities'
        finalData['creation time'] = int(time.time())
        if 'organization' not in finalData:
            finalData['organization'] = dict()

    def getUrl(self, pageNo):
        self.url = "https://www.4icu.org/reviews/index" + str(pageNo) + ".htm"
        self.fetch(self.url)

        unis = self.bts.find('table')
        unis = unis.find_all('tr')

        for uni in unis:
            try:
                td = uni.find_all('td')
                if(len(td) == 2):
                    url = 'https://www.4icu.org' + td[0].find('a').attrs['href']
                    if url not in urlList['url']:
                        urlList['url'][url] = False
            except:
                pass

    def getCountry(self, pageNo):
        self.url = "https://www.4icu.org/reviews/index" + str(pageNo) + ".htm"
        self.fetch(self.url)

        unis = self.bts.find('table')
        unis = unis.find_all('tr')

        for uni in unis:
            try:
                td = uni.find_all('td')
                if(len(td) == 2):
                    country = td[1].find('img').attrs['alt']
                    name = td[0].find('a').text.strip()
                    name = ' '.join([x.strip() for x in name.split()])
                    name = name.lower()
                    finalData['organization'][name]['country'] = country
            except:
                pass


    def getUniData(self, url):
        self.url = url
        self.fetch(self.url)
        # print("page loaded")

        table = self.bts.find_all('table')

        # local data -----------------------------------------
        d = dict()

        try:
            # ranking --------------------------------------------
            rank = table[0].find_all('tr')
            for tr in rank:
                try:
                    x = [x.strip() for x in tr.text.strip().split('\n')]
                    d[x[0].lower()] = ' '.join(x[1:])
                except Exception as e:
                    print(e)

            # identity --------------------------------------------
            identity = table[1].find_all('tr')
            for i in range(6):
                try:
                    title = identity[i].find('th').text
                    data = identity[i].find('td').text
                    title = ' '.join([x.strip().lower() for x in title.split()])
                    data = ' '.join([x.strip() for x in data.split()])
                    if title not in d and title != 'screenshot':
                        d[title] = data
                    if title == 'screenshot':
                        website = identity[i].find('a').attrs['href']
                        d['website'] = website
                except:
                    pass

            # location --------------------------------------------
            location = table[2].find_all('tr')
            for tr in location:
                try:
                    x = [x.strip() for x in tr.text.strip().split('\n')]
                    d[x[0].lower()] = ' '.join(x[1:])
                except Exception as e:
                    print(e)


            # degree available --------------------------------------------
            try:
                degreeNames = [' '.join([x.strip().lower() for x in td.text.strip().split('\n')]) for td in table[3].find('thead').find_all('tr')[1].find_all('td')]
                degreeAvail = [td.find('i').attrs['class'][1].strip() for td in table[3].find('thead').find_all('tr')[2].find_all('td')]

                d['degrees'] = dict()
                for i in range(len(degreeAvail)):
                    if degreeAvail[i] == 'd1':
                        d['degrees'][degreeNames[i]] = list()

                departments = table[3].find('tbody').find_all('tr')
                for department in departments:
                    x = department.find_all('td')
                    name = x[0].find('div').find('a').text.strip()
                    avabl = [x[i].find('i').attrs['class'][1].strip() for i in range(1, 5)]
                    for i in range(len(avabl)):
                        if avabl[i] == 'd1':
                            d['degrees'][degreeNames[i]].append(name)
            except Exception as e:
                print(e)

            # tution fees --------------------------------------------
            try:
                label = [' '.join([i.strip() for i in x.text.strip().split()]) for x in table[4].find('thead').find('tr').find_all('th')]
                local = [x.text.strip() for x in table[4].find('tbody').find_all('tr')[0].find_all('td')]
                inter = [x.text.strip() for x in table[4].find('tbody').find_all('tr')[1].find_all('td')]

                d['tuition fee'] = dict()
                for i in range(1, 3):
                    if label[i] not in d['tuition fee']:
                        d['tuition fee'][label[i].lower()] = dict()
                    d['tuition fee'][label[i].lower()][local[0].lower()] = local[i]
                    d['tuition fee'][label[i].lower()][inter[0].lower()] = inter[i]
            except Exception as e:
                print(e)


            # addmission ---------------------------------------------
            try:
                adinfo = [[x.strip() for x in tr.text.strip().split('\n')] for tr in table[5].find_all('tr')]
                for i in adinfo:
                    d[i[0].lower()] = ' '.join(i[1:])
            except Exception as e:
                print(e)

            # size and profile ---------------------------------------
            try:
                adinfo = [[x.strip() for x in tr.text.strip().split('\n') if x.strip() != ""] for tr in table[6].find_all('tr')]
                for i in adinfo:
                    d[i[0].lower()] = ' '.join(i[1:])

                adinfo = [[x.strip() for x in tr.text.strip().split('\n') if x.strip() != ""] for tr in table[7].find_all('tr')]
                for i in adinfo:
                    d[i[0].lower()] = ' '.join(i[1:])

            except Exception as e:
                print(e)

            # Facilities ----------------------------------------------
            try:
                adinfo = [[x.strip() for x in tr.text.strip().split('\n') if x.strip() != ""] for tr in table[8].find_all('tr')]
                for i in adinfo:
                    d[i[0].lower()] = ' '.join(i[1:])

                adinfo = [[x.strip() for x in tr.text.strip().split('\n') if x.strip() != ""] for tr in table[9].find_all('tr')]
                for i in adinfo:
                    d[i[0].lower()] = ' '.join(i[1:])

            except Exception as e:
                print(e)

            # save data -----------------------------------------------------
            global finalData
            finalData['organization'][d["name"].lower()] = d
            urlList['url'][url] = True
            global totalProcessed
            totalProcessed += 1

            # print("data saved")

            # info ----------------------------------------------------------
            # print(json.dumps(d, indent=2))
            os.system('clear')
            print("-------------------------------------")
            print("Total University loaded:", len(finalData['organization']))
            print("-------------------------------------")

            # write data ----------------------------------------------------
            global processLap
            if int(totalProcessed / 100) > processLap:
                processLap = int(totalProcessed / 100)
                with open('urlList.json', 'w') as f:
                    json.dump(urlList, f, indent=2)
                with open('finalData.json', 'w') as f:
                    json.dump(finalData, f, indent=2)

        except Exception as e:
            print("failed to process data: ", url)
            print("page data procssing exception:", e)

def saveData():
    with open('urlList.json', 'w') as f:
        json.dump(urlList, f, indent=2)
    with open('finalData.json', 'w') as f:
        json.dump(finalData, f, indent=2)
    print("\n-------------------------------------")
    print("Total University data loaded:", len(finalData['organization']))
    print("-------------------------------------\n")

def fetchData():
    with ThreadPoolExecutor(max_workers=10) as executor:
        for url in urlList['url']:
            if urlList['url'][url] == False:
                uni = allUniversityData()
                executor.submit(uni.getUniData, url)
    os.system('clear')
    saveData()

def fetchCountry():
    with ThreadPoolExecutor(max_workers=10) as executor:
        for i in range(2, 28):
            uni = allUniversityData()
            executor.submit(uni.getCountry, i)
    os.system('clear')
    saveData()

def fetchUrl():
    urlList['source'] = "https://www.4icu.org/";
    urlList['description'] = 'List of urls that contain detaild information of all university'
    urlList['creation time'] = int(time.time())
    if 'url' not in urlList:
        urlList['url'] = dict()

    with ThreadPoolExecutor(max_workers=10) as executor:
        for i in range(2, 28):
            uni = allUniversityData()
            executor.submit(uni.getUrl, i)

    os.system('clear')
    print("\n\nTotal", len(urlList['url']), ' url loded\n')

    saveData()

def loadData():
    try:
        with open('urlList.json', 'r') as f:
            global urlList
            urlList = json.load(f)
    except Exception as e:
        print('urlList json loading exception:', e)

    try:
        with open('finalData.json', 'r') as f:
            global finalData
            finalData = json.load(f)
    except Exception as e:
        print('finalData json loading exception:', e)

def main():
    loadData()
    fetchUrl()
    fetchData()
    fetchCountry()

if __name__ == '__main__':
    main()
