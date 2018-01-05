#!/usr/bin/env python
#! usr/bin/python #coding = utf-8
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
        req = urllib2.Request(page, None, {'User-agent' : 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0'})
        content = urllib2.urlopen(req, timeout = 5).read()
    except:
        pass
    return content


def get_douban(isbn):

    start = time.time() # There's some problems with time.clock()
    seed = 'https://api.douban.com/v2/book/isbn/'# sys.argv[1]
    crawled = []
    count = 0
    seed = seed + isbn
    q = Queue.Queue()
    #Start to get book page
    print json.loads(get_page(seed))['author'][0].encode('utf-8')

    end = time.time()
    print end-start, 's'


isbn = raw_input()
get_douban(isbn)