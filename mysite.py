# -*- coding:utf-8 -*-
import web			#import webpy 作为主框架
from web import form		#import form 作为交互信息方法
import re
import os, sys
import SearchFiles_JD		#import search主体代码
from crawler.get_library_info import get_library_info as gli		#import sjtu_library 信息获取代码
from crawler.get_douban import get_douban as gd				#import douban_info 信息获取代码
from ctpn.test import find_bbox as fb					#import 图像搜索代码

#主体网页
urls = (
	'/','index',		#文字搜索主页面
	'/res','result',	#结果展示页面
	'/img','img',		#图像搜索页面
	'/(\d*)','detail',	#详情页面
	)

search_result=[]		#search result 作为全局变量，储存搜索结果

render = web.template.render('templates/')

login = form.Form(
	form.Textbox('keywords'),
	form.Button('submit')
	)

all_books=[]


# def get_douban(isbn):
# 	result = ['name','pic_url','']
# 	return result

# def get_library(isbn):
# 	result = []
# 	return result

class index:
	def GET(self):
		f = login()					#传入表单
		return render.index(f)

class img:
	def GET(self):
		f = login()					#传入表单
		return render.img(f)

class result:
	def GET(self):
		global search_result
		user_data = web.input()				#获得用户关键词
		keyword = user_data.keywords
		print keyword
		
		search_result = SearchFiles_JD.main(keyword)	#获得搜索结果
		for i in range(len(search_result[0])):
			print search_result[0][i]
		return render.result(search_result)		#返回给结果界面

	def POST(self):
		filedir = '/tmp'
		x = web.input(myfile={})			#获得图像搜索图片
		fout = open(filedir+'/'+x.myfile.filename,'wb')
		fout.write(x.myfile.file.read())		#将图片储存在tmp中
		fout.close()
		filepath = filedir+'/'+x.myfile.filename
		global search_result
		print filepath
		
		search_result = SearchFiles_JD.main(fb(filepath))	#将图像识别的结果传入搜索引擎，得到结果
		return render.result(search_result)		#返回给结果页面


class detail:
	def GET(self,order):
		global search_result
		order = int(order)-1
		print order
		isbn = search_result[order][5]			#得到isbn信息
		result = []
		res_douban = gd(isbn)				#通过isbn得到豆瓣信息
		print res_douban
		res_library = gli(isbn)				#通过isbn得到图书馆借阅信息
		
		res_jd = [search_result[order][3],
			  search_result[order][0],
			  search_result[order][1],
			  search_result[order][2],
			  search_result[order][4].replace("\\n", "</br>"),
			  search_result[order][6]]		#将jd信息装在list中
		
		res_dangdang = [search_result[order][9],search_result[order][8]] #将dangdang信息装入list中
		if res_dangdang[0]=='unknown':
			tmp = search_result[order][2]
			res_dangdang[0] = tmp
			
		#将信息全部装入result中，return给详情界面
		result.append(res_douban)
		result.append(res_library)
		result.append(res_jd)
		result.append(res_dangdang)
		result.append(search_result[11:14])
		return render.detail(result)


if __name__ == "__main__":
	app = web.application(urls, globals())			#初始化webpy
	app.run()
	SearchFiles_JD.main()					#初始化lucene
