import os
import json
import sys
import csv

projectPath = os.path.normpath(os.getcwd() + os.sep + os.pardir)
sys.path.append(projectPath)

import ots

class cfOrgList(ots.one_time_scraper):

    def __init__(self):
        self.rheaders = '''
            accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
            accept-encoding: gzip, deflate, br
            accept-language: en-US,en;q=0.9,bn;q=0.8
            cache-control: max-age=0
            cookie: __utmc=71512449; _ga=GA1.2.61060163.1612446062; RCPC=52d90a87c43a3a00a78c5a231904aea9; __atuvc=0%7C14%2C1%7C15%2C0%7C16%2C1%7C17%2C2%7C18; X-User-Sha1=20bc7ef9c29855216001f4be704e3a5ba08f7466; nocturne.language=en; __utmz=71512449.1625203965.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utma=71512449.61060163.1612446062.1625664016.1625667618.8; JSESSIONID=1E33C9ECDFB1C1068220265FC3FD7319-n1; 39ce7=CF5v8KbD; evercookie_cache=wc0z65aq2hgy0kozex; evercookie_etag=wc0z65aq2hgy0kozex; evercookie_png=wc0z65aq2hgy0kozex; 70a7c28f3de=wc0z65aq2hgy0kozex; X-User=3c4bc0630481d0db72fbfda42d418a597fe3201c59141e33df64bba2e2e8240a3a7495ae678b984a; lastOnlineTimeUpdaterInvocation=1625992090766
            dnt: 1
            sec-ch-ua: " Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"
            sec-ch-ua-mobile: ?0
            sec-fetch-dest: document
            sec-fetch-mode: navigate
            sec-fetch-site: none
            sec-fetch-user: ?1
            upgrade-insecure-requests: 1
            user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36
        '''
        super().__init__()
        self.url = "https://codeforces.com/ratings"

    def getOrgList(self):
        # self.from_html()
        self.fetch(self.url)

        orgData = self.bts.find("select", {"name":"organizationId"})
        organizations = orgData.find_all('option')

        orgList = set()

        for organization in organizations:
            name = organization.text.strip()
            if len(name) > 0:
                if name[0].isalpha():
                    name = name.split(',')[0].strip()
                    name = name.split()
                    name = ' '.join(name)
                    if len(name) > 3:
                        orgList.add(name)

        orgList = list(orgList)
        orgList = sorted(orgList)

        print("\n[Total", len(orgList), "Organization data Loaded.]")

        for organization in orgList:
            d = {
                'organization' : organization,
                'country' : ''
            }
            self.results.append(d)

        if len(orgList) > 9000:
            self.to_html()

    def saveFinalData(self):
        finalResult = list()

        with open(projectPath+"/educationalInstituteData.csv", 'r') as csv_file:
            reader = csv.DictReader(csv_file)
            finalData = {}

            for row in reader:
                d = dict(row)
                finalData[d['organization']] = d['country']

            for d in self.results:
                if d['organization'] not in finalData:
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
    cf = cfOrgList()
    cf.getOrgList()
    cf.to_csv()
    cf.saveFinalData()


if __name__ == '__main__':
    main()
