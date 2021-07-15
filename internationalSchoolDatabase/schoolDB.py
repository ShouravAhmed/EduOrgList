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


finalData = dict()

class internationalSchoolDatabase(ots.one_time_scraper):
    def __init__(self):
        super().__init__()
        self.url = ""
        finalData['source'] = "https://www.international-schools-database.com/";
        finalData['description'] = 'Find, research and compare the best international schools'
        finalData['creation time'] = int(time.time())
        if 'organization' not in finalData:
            finalData['organization'] = dict()

    def getCities(self):
        pass


def main():
    # hero-image-form-wrapper
    scbd = internationalSchoolDatabase()


if __name__ == '__main__':
    main()
