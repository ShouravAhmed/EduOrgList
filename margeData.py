import json
import time

def main():
    finalData = dict()
    finalData['source'] = "https://github.com/ShouravAhmed/EduOrgList";
    finalData['description'] = 'Details of educational institutes'
    finalData['creation time'] = int(time.time())
    finalData['organization'] = dict()

    dirr = ['uniAZ', 'bdedu', 'codeforces', 'codeOrg', 'hipoUnilist', 'schoolNameOnly']

    for folder in dirr:
        path = folder + '/finalData.json'
        curData = dict()

        try:
            with open(path, 'r') as f:
                curData = json.load(f)
                print("\nTotal data available in", path, "is :", len(curData['organization']))

        except Exception as e:
            print('finalData json loading exception:', e)
            continue

        for organization in curData['organization']:
            if organization != '':
                if organization not in finalData['organization']:
                    finalData['organization'][organization] = curData['organization'][organization]
                else:
                    x = curData['organization'][organization]
                    for a in x:
                        try:
                            if a != '' and a not in finalData['organization'][organization]:
                                finalData['organization'][organization][a] = curData['organization'][organization][a]
                        except Exception as e:
                            pass

    with open('finalData.json', 'w') as f:
        json.dump(finalData, f, indent=2)

    print("\n----------------------------------------")
    print("Final dataset size:", len(finalData['organization']))
    print("----------------------------------------\n")

if __name__=='__main__':
    main()
