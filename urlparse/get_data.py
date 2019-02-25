import re

import pandas
import urllib3
from bs4 import BeautifulSoup

http = urllib3.PoolManager()

url = 'http://eshukan.com/NoLayoutFee.aspx?typeid=12&hxid=8'
response = http.request('GET', url)
soup = BeautifulSoup(response.data)

soup.prettify()
typelist = []
namelist = []
counts = []

writer = pandas.ExcelWriter("/home/xhyang/src/pydata/统计.xlsx")


def encode(s):
    return int(''.join(map(str, [ord(char) for char in s])))


for anchor in soup.findAll('a', href=True, text=True):
    if "NoLayoutFee.aspx?typeid=" in anchor['href']:
        typelist.append(anchor['href'])
        namelist.append(anchor.text)
        num = int(re.findall('\d+', anchor.text)[0])
        counts.append((num + 59) // 60)

for section, name, pg in zip(typelist, namelist, counts):
    typeid = section.split("?")[1]
    summary = []
    for index in range(1, pg + 1):
        url = "http://eshukan.com/NoLayoutFee.aspx?pg=" + str(
            index) + "&" + typeid
        response = http.request('GET', url)
        soup = BeautifulSoup(response.data)
        for anchor in soup.findAll('li', {'class': 'bu'}):
            for title in anchor.findAll('a', href=True, text=True):
                summary.append(title.text)

    pdsum = pandas.DataFrame(summary)
    print(name)
    pdsum.to_excel(excel_writer=writer, sheet_name=str.replace(name, "/", ""))

    writer.save()
    writer.close()
