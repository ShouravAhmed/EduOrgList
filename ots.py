import requests
from bs4 import BeautifulSoup
import csv
import json
import re
import os

class one_time_scraper(object):
    def __init__(self):
        self.cookies = dict()
        self.rheaders = ""
        # ----------------------------------------------------------
        self.page_htm = None
        self.bts = None
        self.response = None
        # ----------------------------------------------------------
        self.results = list()
        self.prvResults = list()
        # ----------------------------------------------------------
        self.headers = self.parse_headers(self.rheaders)
        self.cookies = self.parse_cookies(self.headers['Cookie'])
        if 'User-Agent' not in self.headers:
            self.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
        # ----------------------------------------------------------

    # --------------------------------------------------------------
    # Scraper
    # --------------------------------------------------------------
    def fetch(self, url, **kwargs):
        try:
            pm = {}
            if 'params' in kwargs:
                pm = kwargs['params']

            res = requests.get(url, headers=self.headers, params=pm)
            print(f"\nHTTP get request to url '{res.url}' | status code {res.status_code}")

            self.response = res
            self.page_htm = res.text
            self.bts = BeautifulSoup(self.page_htm, 'lxml')

            return res.status_code

        except Exception as e:
            print("\nfetch exception:", e)
            return None

    def to_html(self):
        with open('res.html', 'w') as html_file:
            html_file.write(self.bts.prettify())
        print("\nHTML data saved in 'res.html' successfully.")
        return True

    def from_html(self):
        ret = ""
        totalLines = 0
        try:
            with open('res.html', 'r') as html_file:
                for line in html_file.readlines():
                    ret += line
                    totalLines += 1
        except Exception as e:
            print("\nhtml reading exception:", e)
            return None

        if totalLines <= 10:
            return None
        else:
            self.page_htm = ret
            self.bts = BeautifulSoup(self.page_htm, 'lxml')
            print("\n'res.html' fetched successfully.")
            return True

    def to_csv(self):
        with open('res.csv', 'w') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self.results[0].keys())
            writer.writeheader()
            for row in self.results:
                writer.writerow(row)
        print("\nAll data written in 'res.csv' successfully.")

    def from_csv(self):
        with open("res.csv", 'r') as csv_file:
            reader = csv.DictReader(csv_file)
            rdata = []
            for row in reader:
                rdata.append(dict(row))
            self.prvResults = rdata
        print("\nAvailable data loaded from 'res.csv'")


    # --------------------------------------------------------------
    # Headers and Cookies handling
    # --------------------------------------------------------------
    def parse_cookies(self, raw_cookies):
        parsed_cookies = dict()
        # print("\nraw cookies:\n", raw_cookies)

        for item in raw_cookies.split(';'):
            if item.count('=') > 1:
                x = item.split(',')
                for y in x:
                    l = [z.strip() for z in y.strip().split('=')]
                    try:
                        if len(l) > 2:
                            parsed_cookies[l[0]] = "=".join(l[1:])
                        else:
                            pattern = re.compile(r"\w+")
                            regex_match = pattern.search(l[1])
                            if regex_match is None:
                                continue
                            parsed_cookies[l[0]] = l[1]
                    except:
                        pass
            else:
                l = [x.strip() for x in item.strip().split('=')]
                try:
                    pattern = re.compile(r"\w+")
                    regex_match = pattern.search(l[1])
                    if regex_match is None:
                        continue
                    parsed_cookies[l[0]] = l[1]
                except:
                    pass

        # print("\nparsed_cookies:\n", json.dumps(parsed_cookies, indent=2))
        return parsed_cookies

    def parse_headers(self, raw_headers):
        raw_headers = [header.strip() for header in raw_headers.split('\n')]
        parsed_headers = dict()

        for header in raw_headers:
            l = [x.strip() for x in header.split(': ')]
            if len(l) == 2:
                if l[0] == 'cookie':
                    l[0] = 'Cookie'
                parsed_headers[l[0]] = l[1]

        if 'Cookie' not in parsed_headers:
            parsed_headers['Cookie'] = ""

        # print(json.dumps(parsed_headers, indent=2))
        return parsed_headers

    def update_cookies(self):
        set_ck = ""
        if 'Set-Cookie' in self.response.headers:
            set_ck = str(self.response.headers['Set-Cookie'])

        cookies_update = self.parse_cookies(set_ck)

        for x, y in cookies_update.items():
            self.cookies[x] = y
        cookie_string = ""
        for x, y in self.cookies.items():
            if cookie_string == "":
                cookie_string = x+"="+y
            else:
                cookie_string += "; "+x+"="+y

        self.headers['Cookie'] = cookie_string

    # --------------------------------------------------------------
    # --------------------------------------------------------------

def main():
    sc = one_time_scraper()

    if sc.from_html() is None:
        sc.fetch("https://www.google.com/")
        sc.to_html()

    sc.results.append(
        {
            'name' : 'ahmed',
            'email': 'ahmed15-898@diu.edu.bd'
        }
    )
    sc.to_csv()

if __name__ == '__main__':
    main()
