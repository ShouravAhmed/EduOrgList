import json
import time

def margeFinalData():
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
            print(path+'/finalData.json loading exception:', e)
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

def margeBangladeshData():
    with open("finalData.json", 'r') as f:
        finalData = json.load(f)
        bdData = list()
        for organization in finalData['organization']:
            try:
                if finalData['organization'][organization]['country'].strip().lower() == "bangladesh":
                    organizationData = finalData['organization'][organization]
                    d = dict()
                    d['name'] = organizationData['name']
                    d['city'] = None
                    d['state'] = None
                    d['country'] = organizationData['country']
                    try:
                        d['website'] = organizationData['website']
                    except:
                        d['website'] = None

                    address = organizationData['address']
                    addressProcessing = address.split(',')

                    if len(addressProcessing) >= 4 and len(addressProcessing[-2].split()) == 1 and len(addressProcessing[-1].split()) == 1:
                        d['city'] = addressProcessing[-2]
                        d['state'] = addressProcessing[-1]
                    else:
                        addressProcessing = address.split('  ')
                        try:
                            state = addressProcessing[-1].split(' ')[-2]
                            d['state'] = state
                        except:
                            pass
                        try:
                            city = addressProcessing[-2].split(' ')[-1]
                            d['city'] = city
                        except:
                            pass

                    bdData.append(d)
            except:
                pass

    with open('bdData.json', 'w') as f:
        json.dump(bdData, f, indent=2)

    print("\n--------------------------------")
    print("Total data saved in bdData.json is:", len(bdData))
    print("--------------------------------")



def main():
    # margeFinalData()
    margeBangladeshData()

if __name__=='__main__':
    main()
