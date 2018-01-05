# -*- coding:utf-8 -*-
#!/usr/bin/env python
#! usr/bin/python

from bs4 import BeautifulSoup
import threading
import Queue
import time
import sys
import urllib2
import re
import urlparse
import os
import urllib
import json
reload(sys)
sys.setdefaultencoding('utf-8')


def get_page(page):
    content = ''
    try:
        req = urllib2.Request(page, None, {'User-agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'})
        content = urllib2.urlopen(req, timeout = 5).read()
    except:
        pass
    return content


def get_douban(isbn):

    start = time.time() # There's some problems with time.clock()
    seed1 = 'http://opac.lib.sjtu.edu.cn/F/BJ1SYKABU396YF65SG67M48VKN2LURBGL95QMVL6KH4P43ECFJ-11437?func=find-b&request='
    seed2 = '&find_code=WRD&adjacent=Y&local_base=SJT01&x=0&y=0'
    crawled = []
    seed = seed1 + isbn + seed2
    q = Queue.Queue()
    # Start to get book page
    # print json.loads(get_page(seed))['author'][0].encode('utf-8')
    content = get_page(seed)
    soup = BeautifulSoup(content, "html5lib")
    for i in soup.findAll('a'):
        if ('所有单册').decode('utf-8') in i.get_text():
            url = i.get('href', '')

    
    content = get_page(url)
    # print content

    soup2 = BeautifulSoup(content, "html5lib")
    table = soup2.find('table', {'border': '0', 'cellspacing' : '2', 'width' : '1000'})
    cnt = 0
    List = []
    for tr in table.findAll('tr'):
        tmp = []
        if (++cnt == 1):
            continue
        for td in tr.findAll('td'):
            tmp.append(td.get_text())
        List.append(tmp)
    
    for i in List:
        for j in i:
            print j.encode('utf-8')
    end = time.time()
    print end-start, 's'


isbn = raw_input()
get_douban(isbn)

