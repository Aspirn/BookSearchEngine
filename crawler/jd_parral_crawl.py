#/usr/bin/python
#coding=utf-8

'''
python 3
'''

from urllib import request		#import用于post header获得信息
import urllib
import json				#import json 来解析返回的内容
from selenium import webdriver
import random
import time				#import time 来计时
import threading
import queue				#多线程爬虫
import ssl
ssl._create_default_https_context = ssl._create_unverified_context	#防止 ssl 出问题

# 加入user-agent 防止反爬虫
User_Agent = ["Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52"]


file = open('data_prd.txt3263','r')		#读入之前爬去的书url目录
url_l = file.readlines()
file.close()
url_list = queue.Queue()			#放入队列
for i in url_l:
        url_list.put(i)


def crawl_price():
        while True:
                url = url_list.get()
                request_url = "http://p.3.cn/prices/mgets?skuIds=J_"+url[14:len(url)-6]		#抓包得到价格的url
                print(request_url)
                req_url = urllib.request.Request('https:'+url.strip())
                req_url.add_header('User-Agent',random.choice(User_Agent))
                while True:
                    try:
                        res_url = str(urllib.request.urlopen(req_url,timeout = 10).read().decode('gbk','ignore'))
                    except:
                        pass
                    else:
                        break
		#request得到价格的response
                req_price = urllib.request.Request(request_url)
                req_price.add_header("Accept","*/*")
                #req.add_header("Accept-Encoding","gzip, deflate, br")
                req_price.add_header("Accept-Language","zh-CN,zh;q=0.8")
                req_price.add_header("Connection","keep-alive")
                req_price.add_header("Host","p.3.cn")
                req_price.add_header("Referer",('https:'+url).strip())
                req_price.add_header('User-Agent',random.choice(User_Agent))
		
		#request得到网页信息的response
                req_page = urllib.request.Request('https:'+url.strip())
                req_page.add_header("authority","item.jd.com")
                req_page.add_header("method","GET")
                req_page.add_header("path",'/'+url[14:len(url)-6]+'.html')
                req_page.add_header("scheme","https")
                req_page.add_header('accept','text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8')
                req_page.add_header('accept-language','zh-CN,zh;q=0.8')
                req_page.add_header('referer','https://book.jd.com/')
                req_page.add_header('user-agent',random.choice(User_Agent))
		
		#request得到评论的response
                req_comment = urllib.request.Request('https://sclub.jd.com/comment/productPageComments.action?productId='+url[14:len(url)-6]+'&score=0&sortType=3&page=0&pageSize=10&isShadowSku=0')
                req_comment.add_header('user-agent',random.choice(User_Agent))
                req_comment.add_header('authority','sclub.jd.com')
                req_comment.add_header('path','/comment/productPageComments.action?productId='+url[14:len(url)-6]+'&score=0&sortType=3&page=0&pageSize=10&isShadowSku=0')
                req_comment.add_header('method',"GET")
                req_comment.add_header('scheme','https')
                req_comment.add_header('accept','*/*')
                req_comment.add_header('accept-language','zh-CN,zh;q=0.8')
                req_comment.add_header('referer','https:'+url.strip())
		
		# 加入while 判断返回信息是否有误，如果为错误信息，则继续运行request
                while True:
                    try:
                        res_comment = str(urllib.request.urlopen(req_comment,timeout = 10).read().decode('gbk','ignore'))
                    except:
                        pass
                    else:
                        break
                while True:
                    try:
                        res_page = str(urllib.request.urlopen(req_page,timeout = 10).read().decode('gbk','ignore'))
                    except:
                        pass
                    else:
                        break
                while True:
                    try:
                        res_price = str(urllib.request.urlopen(req_price,timeout = 10).read().decode('gbk','ignore'))
                    except:
                        pass
                    else:
                        break
                time.sleep(random.randint(2,5))		#设置等待时间
		
		
                file = open(url[14:len(url)-6]+'price','w')		#将所有信息保存到本地
                file.write(res_price)
                print(res_price)
                file.close()
                file = open(url[14:len(url)-6]+'page','w')
                file.write(res_page+'\n'+res_url)
                file.close()
                file = open(url[14:len(url)-6]+'comment','w')
                file.write(res_comment)
                file.close()
        return

def main():
	for i in range(16):						#开启多线程
                t = threading.Thread(target = crawl_price)
                t.setDaemon(False)
                t.start()
		#price,page,comment,page2 = crawl_price(i)
		#file = open(i[14:len(i)-6]+'price','w')
		#file.write(price)
		#file.close()
		#file = open(i[14:len(i)-6]+'page','w')
		#file.write(page+'\n'+page2)
		#file.close()
		#file = open(i[14:len(i)-6]+'comment','w')
		#file.write(comment)
		#file.close()
	#crawl_price()
main()
