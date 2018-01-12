#/usr/bin/python
#coding=utf-8

# import cv2
# import numpy as np

# img = cv2.imread('test.jpg',0)
# img = cv2.resize(img,(500,800))
# # img = cv2.GaussianBlur(img,(3,3),0)
# canny = cv2.Canny(img,50,150)

# cv2.imshow('Canny',canny)
# cv2.waitKey(0)
#!/usr/bin/python
#coding:utf-8

import cv2
import numpy as np
def get_title_position(url):
	img = cv2.imread(url,0)			#读入照片文件
	img = cv2.resize(img,(500,800))		#resize照片尺寸，便于处理
	
	x = cv2.Sobel(img,cv2.CV_16S,1,0)		#计算sobel算子
	y = cv2.Sobel(img,cv2.CV_16S,0,1)
	absX = cv2.convertScaleAbs(x)
	absY = cv2.convertScaleAbs(y)
	th1 = cv2.addWeighted(absX,0.5,absY,0.5,0)	#得到梯度图像
	# print dst
	# for i in range(0,len(dst)):
	# 	for j in range(0,len(dst[0])):
	# 		if dst[i][j]<100:
	# 			dst[i][j] = 0
	# print dst
	# cv2.imshow("Result",dst)
	# from matplotlib import pyplot as plt
	kernel=np.uint8(np.zeros((3,3)))		#通过otsu方法，二值化图像
	kernel[0][1] = kernel[1][0] = kernel[1][1] = kernel[1][2] = kernel[2][1] = 1
	kernel2=np.uint8(np.zeros((3,3)))
	kernel2[1][0] = kernel2[1][1] = kernel2[1][2] = 1
	#kernel2 = np.array([1,1,1])
	#kernel2 = kernel2.reshape(-1,1)
	print kernel2
	ret1, th1 = cv2.threshold(th1, 0, 255, cv2.THRESH_OTSU)

	th2 = th1
	th1 = cv2.erode(th1,kernel)			#腐蚀图像
	th1 = cv2.dilate(th1,kernel)			#扩张图像
	th1 = cv2.dilate(th1,kernel2,iterations = 10)
	th1 = cv2.erode( th1,kernel2, iterations = 10)
	cv2.imshow('result',th1)
	cv2.waitKey()
	
	contours, hierarchy = cv2.findContours(th1,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)	#得到连通图像
	print contours[0]
	for points in contours:									#得到连通位置
		x,y,w,h = cv2.boundingRect(points)
		if w*h>3000:
			cv2.rectangle(th2,(x,y),(x+w,y+h),(255,255,255),2)
		else:
			continue
	# cv2.drawContours(th1,contours,-1,(255,255,255),3)
	cv2.imshow('result',th2)			#显示结果
	cv2.waitKey()
	return th2
