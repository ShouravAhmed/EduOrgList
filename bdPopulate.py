import json

def populateBdData():
    with open("finalData.json", 'r') as f:
        finalData = json.load(f)
        bdData = list()
        for organization in finalData['organization']:
            try:
                if finalData['organization'][organization]['country'].strip().lower() == "bangladesh":
                    organizationData = finalData['organization'][organization]
                    d = dict()

                    name = organizationData['name']
                    name = ' '.join([x for x in name.split() if x.isalpha()])
                    if name == '':
                        continue

                    d['name'] = name
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

    byName = lambda obj:obj['name']
    bdData = sorted(bdData, key=byName)

    with open('bdData.json', 'w') as f:
        json.dump(bdData, f, indent=2)

    print("\n--------------------------------")
    print("Total Bangladeshi institutes data saved in bdData.json is:", len(bdData))
    print("--------------------------------")

def main():
    populateBdData()


if __name__ == '__main__':
    main()
