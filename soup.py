from bs4 import BeautifulSoup
import re
import csv
import requests
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
htmlPaths = ["html/baby-select-diapering-wall.html",
            "html/baby-select-health.html",
            "html/baby-approved-bath-wall.html",
            "html/baby-select-car-seats.html",
            "html/baby-strollers-on-floor.html",
            "html/baby-select-activity.html",
            "html/nursery-on-platforms.html",
            "html/baby-toys-0-18-months-on-shelves.html",
            "html/prenatal-care.html",
            "html/diaper-bags.html",
            "html/baby-approved-potty-wall.html",
            "html/baby-select-carriers-1.html",
            "html/baby-select-bottles-on-shelf.html"]
allTcins = [];
for file in htmlPaths:
    with open(file) as infile:
        soup = BeautifulSoup(infile, 'html.parser')
        tcin1 = "none"
        tcin2 = "none"
        title = "none"
        for pin in soup.find_all("div", class_="pinWrapper"):
            for desc in pin.find_all("p", class_="pinDescription"):
                title = desc.get_text("|", strip=True)
                test = re.search(r"(?<!\d)\d{6,8}(?!\d)", title)
                if test:
                    tcin1 = test.group()
            for href in pin.find_all("a", class_="Button Module NavigateButton borderless hasText pinNavLink navLinkOverlay"):
                url = href.get('href')
                test = re.search(r"(?<!\d)\d{6,8}(?!\d)", url)
                if test:
                    tcin2 = test.group()
            if tcin1 != "none":
                tcin = tcin1
            else:
                tcin = tcin2
            if tcin != "none":
                print(tcin)
            else:
                print("NO TCIN FOR: " + title)
            allTcins.append(tcin)
            tcin = "none"
            tcin1 = "none"
            tcin2 = "none"
            title = "none"
print("total items: " ,len(allTcins))
payload = {'key': '6bf34d7581ae95886036b732'}
csvRow = ['Concept Store','X','TCIN','DP','X','DESC,BRAND','n/a','any','x','1','X','X','X','X','X','7/18/2016','PRICE','X','7/15/2016','X','Royalston','7/18-9/9/16','Royalston']
with open('tcins.csv', 'wb') as fp:
    a = csv.writer(fp, delimiter=',')
    for tcin in allTcins:
        print("making request for...", tcin)
        r = requests.get('https://www.tgtappdata.com/v1/products/pdp/TCIN/'+tcin, params=payload)
        data = json.loads(r.text)
        dpci = "n/a"
        title = "n/a"
        brand = "n/a"
        if type(data) is list:
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
                            dpci = value2 .split("-")[0]
        csvRow[2] = tcin
        csvRow[3] = dpci
        csvRow[5] = title
        csvRow[6] = brand
        a.writerow(csvRow)
