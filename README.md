# *Educational Organization List*
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![GitHub license](https://img.shields.io/github/license/ShouravAhmed/EduOrgList.svg)](https://github.com/ShouravAhmed/EduOrgList/blob/main/LICENSE)
[![GitHub forks](https://img.shields.io/github/forks/ShouravAhmed/EduOrgList.svg?style=social&label=Fork)](https://github.com/ShouravAhmed/EduOrgList)
[![GitHub stars](https://img.shields.io/github/stars/ShouravAhmed/EduOrgList.svg?style=social&label=Stars)](https://github.com/ShouravAhmed/EduOrgList)

The purpose of this repository is to provide a solution to collect as much as possible detailed list of public data of all educational institute around the World.

### Resource used and their details and solution

* [x] https://www.4icu.org/
  * [uniRank](https://www.4icu.org/) is the leading international higher education directory and search engine featuring reviews and rankings of over 13,800 officially recognized Universities and Colleges in 200 countries.
  * Possible solutions
    * `https://www.4icu.org/reviews/index2.htm` to `index2.htm` this 26 page contain only the *name and country* of all these universities, which can be collected by simple scraping. But these doesn't contain any other information.
    * In the above mentioned solution we can also fetch link for each of these universities which contain detailed information. But problem is we want to scrape those data we have to call more then 13800 times, 1 call per university. We can make it faster by threading but overall process will be quite slow.
  * Implemented solution
    * `EduOrgList/uniAZ` contain the implementation of possible solution 2.
    * `uniaz.py` is the scraper, `urlList.json` contains the list links yet to be process with is-processed status and `finalData.json` contains all the data fetched so far.
    * This scraper update the local files after fetching each new 100 university data, `urlList.json` with is-processed status for links and `finalData.json` with new data. So, if scraper stop in some point data will be safe and after running the scraper again it will start from the same point where it stopped.
    * Data fetched for each universities are "country rank", "world rank", "name", "acronym", "founded", "motto", "colours", "address", "tel", "fax", "other locations", "degrees", "tuition fee", "gender", "international students", "selection type", "admission rate", "admission office", "student enrollment", "academic staff", "control type", "entity type", "academic calendar", "campus setting", "religious affiliation", "library", "housing", "sport facilities", "financial aids", "study abroad", "distance learning", "academic counseling", "career services" and "institutional hospital" status.
* [x] https://banbeis.portal.gov.bd/
  * [BANBEIS](https://banbeis.portal.gov.bd/) is Bangladesh Bureau of Educational Information and Statistics is the only government agency responsible for the collection and dissemination of statistics and information in Bangladesh. It contains data for total 34917 different institute.
  * Possible solutions
    * Their web site contains school, college, school and college, madrasa, technical college, private and public university data in separate `.xlsx` file. We can read all these files using `openpyxl` python module and covert and write those data in more suitable format.
  * Implemented solution
    * First all the `.xlsx` files are downloaded and placed into `EduOrgList/bdedu`.
    * Data scraper is the `bdedu.py`. Using `openpyxl` python module we read all data and write them in `finalData.json` file.
    * Data available for each organization are "name", "address", "country" and "tel".
* [x] https://code.org/learn/find-school/json
  * [Code.org](https://code.org) is a non-profit organization and eponymous website that aims to encourage people, particularly school students to learn computer programming. Code.org provide public JSON access to the database that powers the Code.org local school search. API link is https://code.org/schools.json. Total data available 5314.
  * Possible solutions
    * We can simply grab the json and take necessary information we need.
    * Data they provide for each school is "name", website", "levels", "format", "format_description", "gender", "description", "languages", "money_needed", "online_only", "number_of_students", "contact_name", "contact_number", "contact_email", "latitude", "longitude", "street", "city", "state", "zip", "published", "updated_at", "country", "source"
  * Implemented solution
    * They provide many unnecessary data that doesn't necessary for general propose, so I grabbed necessary data and write them in `finalData.json` in the same format as we did for other sources.
    * Grabbed data are "name", "website", "gender", "student enrollment", "tel", "email", "address" and "country".
* [x] https://codeforces.com/api/user.ratedLis
  * [Codeforces](https://codeforces.com/) is a website that hosts competitive programming contests. It has over 600,000 registered users.
  * Possible solution
    * Codeforces provide public api access to grab their data. We can fetch all user profile (600000+) data from this api. User profile contain the data of Educational institute or organization the user belong and it's address and country. In this solution problem is the organization name users provided could be imaginary and the address also could be fake. And useful information only can garbed is Organization name, address, country.
  * Implemented solution
    * From the API I grabbed the data mentioned above and write them in `rawData.json` and after processing it saved the final data in `finalData.json`, in the same format as we did for other sources.
    * `rawData.json` is not uploded because of this size `150+ mb`. Here is the `rawData.json` manual [Download link](https://drive.google.com/file/d/1GquQxqgedmO_Tut2tAXa5_yBQXT1XyJ3/view?usp=sharing).
    * Grabbed data are "name", "address" and "country". Total valid data grabbed is 7962.

### Other public resource and API's

* [x] https://github.com/EricTendian/colleges-master-list
* [x] https://github.com/MLH/mlh-policies/blob/master/schools.csv
* [x] https://raw.githubusercontent.com/Hipo/university-domains-list/master/world_universities_and_domains.json
* [x] https://github.com/endSly/world-universities-csv
* [x] https://www.international-schools-database.com/ Data of all international schools in big cities (can be scraped).
* [x] https://developer.schooldigger.com/ U.S. K-12 schools and district data.
* [x] https://www.greatschools.org/api/ U.S. K-12 schools database.
* [x] https://educationdata.urban.org/documentation/ U.S schools.
* [x] https://collegescorecard.ed.gov/data/documentation/ U.S data.

most of the available API's are only U.S or U.K based and paid, some allow access with limited call.
