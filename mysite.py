# -*- coding:utf-8 -*-
import web
from web import form
import re
import os,sys
import SearchFiles_JD
from get_library_info import get_library_info as gli
from get_douban import get_douban as gd
from ctpn.test import find_bbox as fb
urls = (
	'/','index',
	'/res','result',
	'/img','img',
	'/(\d*)','detail',
	)
search_result=[]

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
		f = login()
		return render.index(f)

class img:
	def GET(self):
		f = login()
		return render.img(f)

class result:
	def GET(self):
		global search_result
		user_data = web.input()
		keyword = user_data.keywords
		print keyword
		search_result = SearchFiles_JD.main(keyword)
		for i in range(len(search_result[0])):
			print search_result[0][i]
		return render.result(search_result)

	def POST(self):
		filedir = '/tmp'
		x = web.input(myfile={})
		fout = open(filedir+'/'+x.myfile.filename,'wb')
		fout.write(x.myfile.file.read())
		fout.close()
		filepath = filedir+'/'+x.myfile.filename
		global search_result
		print filepath
		search_result = SearchFiles_JD.main(fb(filepath))
		return render.result(search_result)


class detail:
	def GET(self,order):
		global search_result
		order = int(order)-1
		print order
		isbn = search_result[order][5]
		result = []
		res_douban = gd(isbn)
		print res_douban
		res_library = gli(isbn)
		res_jd = [search_result[order][3],search_result[order][0],search_result[order][1],search_result[order][2],search_result[order][4].replace("\\n", "</br>"),search_result[order][6]]
		res_dangdang = [search_result[order][9],search_result[order][8]]
		if res_dangdang[0]=='unknown':
			tmp = search_result[order][2]
			res_dangdang[0] = tmp
		result.append(res_douban)
		result.append(res_library)
		result.append(res_jd)
		result.append(res_dangdang)
		result.append(search_result[11:14])
		return render.detail(result)


if __name__ == "__main__":
	app = web.application(urls, globals())
	app.run()
	SearchFiles_JD.main()