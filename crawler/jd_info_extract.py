#/usr/bin/python
#coding=utf-8

import json
import os
import sys
from bs4 import BeautifulSoup


path = 'D:\\Book Search Project\\11047'		#获得路径下所有文件
all_file = os.listdir(path)
file1 = open('result','w',encoding='utf-8')
#for i in range(15000,len(all_file)):

for i in range(0,len(all_file)):		#便利所有文件
	# all_book = {}
	if 'price' not in all_file[i]:		#只搜寻有价格的图书
		continue
	id = all_file[i][:-5]			#获得图书id
	print(id)

	file = open(path+'\\'+id+'price','r')
	price = file.readline()
	file.close()
	if 'error' in price:			#判断价格信息是否有误
		prices=[-1,-1]
	else:
		try:
			price = json.loads(price)
			prices = [price[0]['op'],price[0]['p']]
		except:
			prices=[-1,-1]

	file = open(path+'\\'+id+'page','r')	#读取网页信息
	page = '\n'.join(file)
	file.close()
	
	author_begin = page.find('authors')	#获得作者
	author_end = page.find(']',author_begin)
	author = page[author_begin+10:author_end]
	
	type_begin = page.find('catName')	#获得目录
	type_end = page.find(']',type_begin)
	type = page[type_begin+10:type_end]
	soup = BeautifulSoup(page)
	imgurl = soup.find('img',{'data-img':'1'})	#获得封面图片
	detail = str(soup.find('ul',{'id':'parameter2'}))
	try:
		tag = soup.find('meta',{'name':'keywords'})['content']
	except:
		tag = ''
	if imgurl:
		title = imgurl['alt']		#获得keywords
		imgurl = imgurl['src']
	else:
		title = imgurl = 'unknown'

	try:
		file = open(path+'\\'+id+'comment','r')		#获得评论信息
		content = file.readlines()
		file.close()
		data = json.loads(content[0])
		comment_number = len(data['comments'])		
		comments = []
		comments.append([data['productCommentSummary']['goodRate'],		#好评率
					data['productCommentSummary']['goodCount'],	#好评数
					data['productCommentSummary']['generalRate'],	#中评率
					data['productCommentSummary']['generalCount'],
					data['productCommentSummary']['poorRate'],	#差评
					data['productCommentSummary']['poorCount']])
		for i in range(comment_number):
			comments.append([[],[]])
			comments[i+1][0].append(data['comments'][i]['content'])		#评论内容和图片
			if 'images' in data['comments'][i]:
				img = data['comments'][i]['images']
				for j in range(len(img)):
					comments[i+1][1].append(img[j]['imgUrl'])
	except:
		commands = []
	# all_book[id] = [title,author,type,prices,imgurl,comments,detail,tag]
	file1.write(title+'\n')								#写入文件，提供索引内容
	file1.write(author+'\n')
	file1.write(type+'\n')
	file1.write(str(prices)+'\n')
	file1.write(imgurl+'\n')
	file1.write(str(comments)+'\n')
	file1.write(str(detail)+'\n')
	file1.write(tag+'\n'*2)
file1.close()
