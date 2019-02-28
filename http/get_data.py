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


def construct_list():
    for anchor in soup.findAll('a', href=True, text=True):
        if "NoLayoutFee.aspx?typeid=" in anchor['href']:
            typelist.append(anchor['href'])
            namelist.append(anchor.text)
            num = int(re.findall('\d+', anchor.text)[0])
            counts.append((num + 59) // 60)


def construct_second_list():
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
                    data = get_data('http://eshukan.com/' + title['href'])
                    print(data)
                    summary.append(title['title'] + "\n:" + data)

        pdsum = pandas.DataFrame(summary)
        print(name)
        pdsum.to_excel(
            excel_writer=writer, sheet_name=str.replace(name, "/", ""))

        writer.save()
        writer.close()


def get_data(url):
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    referer = 'http://eshukan.com/'
    headers = {'User-Agent': user_agent, 'Referer': referer}

    response = http.request('GET', url, headers=headers)
    soup = BeautifulSoup(response.data)
    data = ""
    for anchor in soup.findAll('div', {'class': 'zgcon'}):
        for section in anchor.findAll(
                'p',
            {
                'style': [
                    'text-indent: 32px;line-height: 24px;vertical-align: baseline',
                    'LINE-HEIGHT: 24px; TEXT-INDENT: 32px', 'text-indent:32px',
                    'text-indent: 32px', 'text-indent: 136px',
                    'margin-left:56px', 'text-indent:32px;line-height:24px',
                    'text-indent: 32px;line-height: 24px', 'margin-left:72px',
                    'text-indent:39px', 'margin-left:64px', 'margin-left:53px',
                    'margin-left:29px;text-indent:24px', 'margin-left:60px',
                    'margin-left:59px'
                ]
            },
                limit=5):
            #for content in section.findAll('span'):
            if section.text is not None:
                data += section.text + "\n"

    return data


construct_list()
construct_second_list()
#get_data("http://eshukan.com/displayj.aspx?jid=8184")
