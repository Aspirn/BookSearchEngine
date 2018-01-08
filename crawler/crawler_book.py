# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
from Queue import Queue
import urllib2, urlparse, urllib
import cookielib
import re
import os, sys
import threading
import time
import bloomfilter

def valid_filename(s):
    import string
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    s = ''.join(c for c in s if c in valid_chars)
    return s

def get_page(page, opener, temp):
    #response = urllib2.urlopen(page, timeout = 10)
    postdata = urllib.urlencode({	#根据发出数据模拟request-body
       'r' : "comment/list",
       'productId' : temp,
       'categoryPath' : '01.12.41.00.00.00',
       'mainProductId' : temp,
       'mediumId' : '0',
       'pageIndex' : '1',
       'sortType' : '1',
       'filterType' : '1',
       'isSystem' : '1',
       'tagId' : '0',
       'tagFilterCount' : '0'
    })
    req = urllib2.Request(url = page, data = postdata)
    response = urllib2.urlopen(req)
    content = response.read()
    return content

def get_all_links(content, page):
    title = ""
    price = 0
    picture = []
    comment = []
    soup = BeautifulSoup(content, "html.parser")
    for p in soup.findAll('p',{'id': "dd-price"}):
        tmp = p.getText().split()
        try:
            price = float(tmp[1])
        except:
            price = float(tmp[0][1:])
    for pic in soup.findAll('img',{'id': "largePic"}):
        picture.append(str(pic.get('src')))
    for t in soup.findAll('div', {'class': "name_info"}):
        for ti in t.findAll('h1'):
            title = ti.get('title').encode("utf-8")
    for c in soup.findAll('div', {'id': "comment_list"}):
        for re in c.findAll('a'):
            comment.append(re)
    return title, price, picture, comment
        
def union_dfs(a,b):
    for e in b:
        if e not in a:
            a.append(e)
            
def union_bfs(a,b):
    for e in b:
        if e not in a:
            a[0:0] = [e]
       
def add_page_to_folder(t, page, p, pic, com, content): 
    index_filename = 'books_detail.txt'    
    folder = 'html'                 
    filename = valid_filename(page) 
    index = open(index_filename, 'a')
    index.write(t + '\t' + page + '\t' + str(p) + '\t' + str(len(pic)) + '\t')
    for ele in pic:
        index.write(ele + '\t')

    index.write('\n')
    index.close()
    
    if not os.path.exists(folder):  
        os.mkdir(folder)
    f = open(os.path.join(folder, filename), 'w')
    f.write(content)               
    f.close()



def crawl(seed, max_page, opener):
    global tocrawl, crawled, graph, count, crawling, varLock, m, Hashlist
    varLock = threading.Lock()
    tocrawl = Queue()
    file = open("index_books.txt", 'r')
    for line in file.readlines():
        a = line.strip()
        tocrawl.put(a)
    file.close()
    crawled = []
    graph = {}
    count = 0
    NUM = 100
    m = 2000000
    Hashlist = [0] * m
    crawling = [''] * NUM


    def working(max_page):
        while True:
            page = tocrawl.get()
            temp = int(page[28:-5])
            if not bloomfilter.isInHash(Hashlist, temp, m):
                crawling[int(threading.current_thread().getName())] = page
                
                print str(len(crawled)) + ' ' + page
                
                try:
                    content = get_page(page, opener, temp)
                except Exception, e:
                    #print e
                    crawling[int(threading.current_thread().getName())] = ''
                    continue

                if varLock.acquire():
                    #if len(crawled) >= int(max_page):
                    #    varLock.release()
                    #    break
                    #else:
                    bloomfilter.putData(Hashlist, temp, m)
                    varLock.release()

                #add_page_to_folder(page, content)
                t, p, pic, com = get_all_links(content, page)
                if t != '':
                    add_page_to_folder(t, page, p, pic, com, content)
                #    tocrawl.put(link)
                crawling[int(threading.current_thread().getName())] = ''
                print 'finish ' + page
    threads = []
    for i in range(NUM):
        t = threading.Thread(target=working, name=str(i), args=(max_page,))
        t.setDaemon(True)
        threads.append(t)
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    return graph, crawled



if __name__ == '__main__':
    seed = "http://book.dangdang.com/"
    max_page = 2000000
    max_page = int(max_page)
    start_time = time.time()
    cj = cookielib.CookieJar()	#初始化cookie
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    header=\
        {
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
        }
    head=[]
    for key,value in header.items():
        elem=(key,value)
        head.append(elem)
    opener.addheaders=head
    opener.open(seed)
    graph, crawled = crawl(seed, max_page, opener)
    delta_time = time.time() - start_time
    print str(delta_time) + 's'
    print len(crawled),'pages crawled' 
