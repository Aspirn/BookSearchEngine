import json
import os
import sys
from bs4 import BeautifulSoup

path = 'D:\\Book Search Project\\11047'
all_file = os.listdir(path)
file1 = open('result','w',encoding='utf-8')
#for i in range(15000,len(all_file)):
for i in range(0,len(all_file)):
	# all_book = {}
	if 'price' not in all_file[i]:
		continue
	id = all_file[i][:-5]
	print(id)

	file = open(path+'\\'+id+'price','r')
	price = file.readline()
	file.close()
	if 'error' in price:
		prices=[-1,-1]
	else:
		try:
			price = json.loads(price)
			prices = [price[0]['op'],price[0]['p']]
		except:
			prices=[-1,-1]

	file = open(path+'\\'+id+'page','r')
	page = '\n'.join(file)
	file.close()
	author_begin = page.find('authors')
	author_end = page.find(']',author_begin)
	author = page[author_begin+10:author_end]
	type_begin = page.find('catName')
	type_end = page.find(']',type_begin)
	type = page[type_begin+10:type_end]
	soup = BeautifulSoup(page)
	imgurl = soup.find('img',{'data-img':'1'})
	detail = str(soup.find('ul',{'id':'parameter2'}))
	try:
		tag = soup.find('meta',{'name':'keywords'})['content']
	except:
		tag = ''
	if imgurl:
		title = imgurl['alt']
		imgurl = imgurl['src']
	else:
		title = imgurl = 'unknown'

	try:
		file = open(path+'\\'+id+'comment','r')
		content = file.readlines()
		file.close()
		data = json.loads(content[0])
		comment_number = len(data['comments'])
		comments = []
		comments.append([data['productCommentSummary']['goodRate'],
					data['productCommentSummary']['goodCount'],
					data['productCommentSummary']['generalRate'],
					data['productCommentSummary']['generalCount'],
					data['productCommentSummary']['poorRate'],
					data['productCommentSummary']['poorCount']])
		for i in range(comment_number):
			comments.append([[],[]])
			comments[i+1][0].append(data['comments'][i]['content'])
			if 'images' in data['comments'][i]:
				img = data['comments'][i]['images']
				for j in range(len(img)):
					comments[i+1][1].append(img[j]['imgUrl'])
	except:
		commands = []
	# all_book[id] = [title,author,type,prices,imgurl,comments,detail,tag]
	file1.write(title+'\n')
	file1.write(author+'\n')
	file1.write(type+'\n')
	file1.write(str(prices)+'\n')
	file1.write(imgurl+'\n')
	file1.write(str(comments)+'\n')
	file1.write(str(detail)+'\n')
	file1.write(tag+'\n'*2)
file1.close()