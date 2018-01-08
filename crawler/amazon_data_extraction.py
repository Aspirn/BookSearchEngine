#coding=utf-8
from bs4 import BeautifulSoup
import os
import sys

#get url data
indexDataFile = open('amazon_index.txt', 'r')
indexData = []
count = 0
indexData.append('0')
for i in indexDataFile.readlines():
    tmp = i.split(' ')
    while (count < int(tmp[0]) - 1):
        count += 1
        indexData.append(str(count))
    indexData.append(i)
    count += 1
indexDataFile.close()

#write all information to data.txt
f = open('amazon_data.txt', 'a')

#where the html files lie
dir = 'amazon_html'
files = os.listdir(dir)

#extract all information needed from each file
p = 0
for filename in files:
    if not 'http' in filename.split('.')[1]:
        continue
    print filename
    path = os.path.join(dir, filename)
    file = open(path)
    soup = BeautifulSoup(file.read(), 'html.parser')
    EBook = True
    inf = ''
    #find title(book name)
    titleTmp = soup.find('h1', {'id' : 'title'})
    title = titleTmp.find('span', {'class' : 'a-size-extra-large'})
    if title == None:
        title = titleTmp.find('span', {'class' : 'a-size-large'})
        EBook = False
    title = title.string.encode('utf-8')
    print '##title : ', title
    inf += title + ' '

    #write url
    url = indexData[int(filename.split('.')[0])].split(' ')[1]
    print '##url : ', url
    inf += url + ' '

    #find price
    if EBook == False:
        priceTmp = soup.find('li', {'class' : 'swatchElement selected'})
        price = priceTmp.find('span', {'class' : 'a-size-base a-color-price a-color-price'}).string.split()[0].encode('utf-8')
    else:
        priceTmp = soup.find('ul', {'class' : 'a-unordered-list a-nostyle a-button-list a-horizontal'})
        price = priceTmp.find('span', {'class' : 'a-color-price'}).string.split()[0].encode('utf-8')
    
    print '##price : ', price
    inf += price + ' '

    #find image
    imgsrcTmp = soup.find('div', {'id' : 'main-image-container', 'class' : 'a-column a-span12 a-text-center maintain-height a-span-last'})
    if imgsrcTmp == None:
        imgsrcTmp = soup.find('div', {'id' : 'ebooks-main-image-container', 'class' : 'a-column a-span12 a-text-center maintain-height a-span-last'})
    imgsrc = imgsrcTmp.find('img').get('data-a-dynamic-image', '').split('"')[1].encode('utf-8')
    print '##imgsrc : ', imgsrc
    inf += '1 ' + imgsrc + ' '

    #find comment
    comment = []
    for i in soup.findAll('div', {'data-hook' : 'review-collapsed'}):
        commentTmp = i.string
        if commentTmp != None:
            comment.append(commentTmp.encode('utf-8'))
    # print comment
    if len(comment) > 0:
        inf += str(len(comment)) + ' '
        for i in comment:
            inf += i + ' '
    else:
        inf += '1 目前还没有用户评论'

    f.write(inf + '\n')
    p += 1
    #for test
    # break

print p
f.close()