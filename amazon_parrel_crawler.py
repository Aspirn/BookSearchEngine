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
reload(sys)
sys.setdefaultencoding('utf-8')


def valid_filename(s):
    import string
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    s = ''.join(c for c in s if c in valid_chars)
    return s

def get_page(page):
    content = ''
    try:
        req = urllib2.Request(page, None, {'User-agent' : 'Customer User Agent'})
        content = urllib2.urlopen(req, timeout = 5).read()
    except:
        pass
    return content

def get_all_book_links(soup):

    global count

    for i in soup.findAll('li', {'class': 's-result-item celwidget '}):
        try:
            book_tag = i.find('a', {'class': 'a-link-normal a-text-normal'})
            book_page = book_tag.get('href', '')
            print 'HERE IS HREF: ', book_page
            count += 1
            print '#COUNT: ', count
            add_page_to_folder(book_page)
            print '&Add to file: ', book_page, 'DONE'
        except:
            pass
            
def get_next_page(soup):

    next_page = ''
    try:
        bottom_tag = soup.find('div', {'class': 'pagnHy'})
        next_page_tag = bottom_tag.find('a', {'class': 'pagnNext'})
        next_page = urlparse.urljoin(seed, next_page_tag.get('href', ''))
    except:
        next_page = ''
    return next_page
       
def add_page_to_folder(page):

    global count
    content = get_page(page)
    index_filename = 'amazon_index.txt'
    folder = 'amazon_html'
    try:
        filename = str(count) + '.' + valid_filename(page)
    except:
        filename = str(count) + '.'

    if not os.path.exists(folder):
        os.mkdir(folder)

    try:
        #Add page content into folder
        f = open(os.path.join(folder, filename), 'w')
        f.write(content)
        f.close()

        #Add page number and url into txt
        index = open(index_filename, 'a')
        index.write(str(count) + ' ' + page.encode('ascii', 'ignore') + '\n')
        index.close()
    except:
        pass


def crawling():

    global count
    while not q.empty():

        page = q.get()
        if page not in crawled:
            crawled.append(page)
            content = get_page(page)
            soup = BeautifulSoup(content, 'html.parser')
            #Add next page to queue if it exists
            tmp = get_next_page(soup)
            if tmp != '':
                print '$next page: ', tmp
                q.put(tmp)
            #Subtract the book page from list page
            get_all_book_links(soup)

if __name__ == '__main__':

    start = time.time() # There's some problems with time.clock()
    seed = 'https://www.amazon.cn/'# sys.argv[1]
    crawled = []
    count = 0
    q = Queue.Queue()
    content = get_page('https://www.amazon.cn/gp/book/all_category/')
    soup = BeautifulSoup(content, 'html.parser')
    #Get links of all categories
    for i in soup.findAll('div', {'class': 'a-column a-span9 a-text-center'}):
        for j in i.findAll('a', {'class': 'a-link-nav-icon'}):
            page =urlparse.urljoin(seed, j.get('href', ''))
            q.put(page)
            print page
    print 'getting categories done'
    #Start to get book page
    crawling()

    end = time.time()
    print end-start, 's'
