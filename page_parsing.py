#! /usr/bin/python
# -*- coding: utf8 -*-
from bs4 import BeautifulSoup
import requests
import time
import pymongo

client = pymongo.MongoClient('localhost', 27017)
DB58 = client['db58']
url_list = DB58['url_list']
item_info = DB58['item_info']

#spider 1
def get_links_from(channel, pages, who_sells=0):
    # 拼接完整url
    # 格式： http://bj.58.com/pbdn/1/pn3
    list_view = '{}{}/pn{}/'.format(channel, str(who_sells), str(pages))
    wb_data = requests.get(list_view)
    time.sleep(1)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    if soup.find('td', 't'):
        for link in soup.select('td.t a.t'):
            item_link = link.get('href')
            url_list.insert_one({
                'url': item_link
            })
            print item_link
    else:
        pass

#spider 2
def get_item_info(url):
    wb_data = requests.get(url)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    no_longer_exist = False if soup.find('p', class_="et") == None else True
    if no_longer_exist:
        pass
    else:
        title = soup.title.text
        price = soup.select('span.price.c_f50')[0].text
        date = soup.select('.time')[0].text
        area = list(soup.select('.c_25d a')[0].stripped_strings) if soup.find_all('span', 'c_25d') else None

        item_info.insert_one({
            'title': title,
            'price': price,
            'date': date,
            'area': area
        })
        print({
            'title': title,
            'price': price,
            'date': date,
            'area': area
        })

if __name__ == '__main__':
    get_links_from('http://bj.58.com/diannao/', 3, 0)
    #get_item_info('http://bj.58.com/pingbandiannao/31504787428653x.shtml')
