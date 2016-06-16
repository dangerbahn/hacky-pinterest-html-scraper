from bs4 import BeautifulSoup
import re
import csv
import requests
import json
import sys
import os
import webbrowser
reload(sys)
sys.setdefaultencoding('utf-8')
# url = "https://www.pinterest.com/heatherhortone/baby-approved-car-seats/"
# webbrowser.open(url, new=0, autoraise=True)
htmlPaths = os.listdir("html")
allTcins = [];
for file in htmlPaths:
    with open('html/'+file) as infile:
        soup = BeautifulSoup(infile, 'html.parser')
        tcin1 = "n/a"
        tcin2 = "n/a"
        title = "n/a"
        for pin in soup.find_all("div", class_="pinWrapper"):
            for desc in pin.find_all("p", class_="pinDescription"):
                title = desc.get_text("|", strip=True)
                test = re.search(r"(?<!\d)\d{6,8}(?!\d)", title)
                if test:
                    tcin1 = test.group()
            for href in pin.find_all("a", class_="Button Module NavigateButton borderless hasText pinNavLink navLinkOverlay"):
                url = href.get('href')
                test = re.search(r"(?<!\d)\d{6,8}(?!\d)", url)
                testForPlp = re.search(r"clearCategId", url)
                if test:
                    tcin2 = test.group()
                if testForPlp:
                    tcin2 = "n/a"
            if tcin1 != "n/a":
                tcin = tcin1
            else:
                tcin = tcin2
            if tcin == "n/a":
                tcin = "NO TCIN FOR: " + title
                print("NO TCIN FOR: " + title)
            allTcins.append(tcin)
            tcin = "n/a"
            tcin1 = "n/a"
            tcin2 = "n/a"
            title = "n/a"
print("total items: " ,len(allTcins))
payload = {'key': '6bf34d7581ae95886036b732'}
csvRow = ['Concept Store','X','TCIN','DP','X','DESC','BRAND','n/a','any','x','1','X','X','X','X','X','7/18/2016','PRICE','X','7/15/2016','X','Royalston','7/18-9/9/16','Royalston','scene7 image path not found']
filteredTcins = []
for originaltcin in allTcins:
    tcinAlreadyFound = 'no'
    for checkDuplicate in filteredTcins:
        if originaltcin.isdigit() and checkDuplicate.isdigit():
            if int(originaltcin) == int(checkDuplicate):
                tcinAlreadyFound = 'yes'
    if tcinAlreadyFound == 'no':
        filteredTcins.append(originaltcin)
print("total filtered tcins: " ,len(filteredTcins))
with open('tcins.csv', 'wb') as fp:
    a = csv.writer(fp, delimiter=',')
    detectedChildren = []
    for tcin in filteredTcins:
        print("making request for...", tcin)
        dpci = "n/a"
        title = "n/a"
        brand = "n/a"
        data = "n/a"
        if tcin.isdigit():
            r = requests.get('https://www.tgtappdata.com/v1/products/pdp/TCIN/'+tcin, params=payload)
            data = json.loads(r.text)
        hasAlreadyAddedTcins = 'no'

        if type(data) is list:
            isColor = 'none'
            colors = []
            childTcins = []
            for key, value in data[0].items():
                if key == 'dpci':
                    dpci = value.split("-")[0]
                if key == 'title':
                    title = value
                if key == 'manufacturingBrand':
                    brand = value
                if key == 'variations':
                    for key2, value2 in value[0].items():
                        if key2 == 'dpci':
                            dpci = value2.split("-")[0]
                if key == 'variationDimensions':
                    if value['dimension1']:
                        if value['dimension1'] == 'COLOR':
                            isColor = 'dimension1'
                    try:
                        if value['dimension2']:
                            if value['dimension2'] == 'COLOR':
                                isColor = 'dimension2'
                    except KeyError:
                        # Key is not present
                        pass

                if key == 'variations':

                    for t in range(len(value)):
                        colorAlreadyAdded = 'no'
                        for key5, value5 in value[t].items():
                            if key5 == 'variationValues':
                                if (isColor == 'dimension1') or (isColor == 'dimension2'):
                                    for clr in colors:
                                        if clr == value5[isColor]:
                                            colorAlreadyAdded = 'yes'
                                    if colorAlreadyAdded == 'no':
                                        colors.append(value5[isColor])
                                        for key4, value4 in value[t].items():
                                            if key4 == 'tcin':
                                                currentVaraitionTcin = int(value4)
                                                childTcins.append(currentVaraitionTcin)
                    if (isColor == 'dimension1') or (isColor == 'dimension2'):
                        hasAlreadyAddedTcins = 'yes'
                        for childItem in range(len(childTcins)):
                            newRow = csvRow
                            newRow[2] = childTcins[childItem]
                            newRow[3] = dpci
                            newRow[5] = title
                            newRow[6] = brand
                            newRow[24] = "http://scene7.targetimg1.com/is/image/Target/"+str(childTcins[childItem])
                            a.writerow(newRow)
        if hasAlreadyAddedTcins == 'no':
            csvRow[2] = tcin
            csvRow[3] = dpci
            csvRow[5] = title
            csvRow[6] = brand
            if tcin != "n/a":
                csvRow[24] = "http://scene7.targetimg1.com/is/image/Target/"+tcin
            a.writerow(csvRow)
