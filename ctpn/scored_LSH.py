import cv2
import numpy
import os
import scored_SIFT as ss

def CalcRGB(img):
	b, g, r = cv2.split(img)
	b = numpy.sum(b) 
	g = numpy.sum(g)
	r = numpy.sum(r)
	all  = b + g + r
	res = [0.0,0.0,0.0]
	res[0] = (b + 0.0) / all
	res[1] = (g + 0.0) / all
	res[2] = (r + 0.0) / all
	return res

def CalcP(imgurl):
    P = []
    img = cv2.imread(imgurl, 1)
    h = img.shape[0]
    w = img.shape[1]  
    P += CalcRGB(img[0 : h / 2, 0 : w / 2])
    P += CalcRGB(img[h / 2 : h, 0 : w / 2])
    P += CalcRGB(img[0 : h / 2, w / 2 : w])
    P += CalcRGB(img[h / 2 : h, w / 2 : w])

    low = 0.32
    high = 0.35

    for i, p in enumerate(P):
        P[i] = 0
        if(p > low and p < high):
            P[i] = 1
        elif(p >= high):
            P[i] = 2
    return P

def CalcLSH(p,Sub):

	I = [[] for i in range(12)]

	for i in Sub:
		I[(i - 1) / 2].append(i)
	lsh = []

	for ind in range(12):
		if(len(I[ind]) == 0):
			continue
		for i in I[ind]:
			lsh.append(0 + (i - 2 * ind <= p[ind]))

	return lsh

def Initializing(Sub):

	files = os.listdir('dataset')
	allHash = []
	allHashFileID = []
	allP = []

	for i in range(len(files)):
		imgurl = 'dataset/' + files[i]
		p = CalcP(imgurl)
		allP.append(p)
		lsh = CalcLSH(p,Sub)
		if(lsh in allHash):
			allHashFileID[allHash.index(lsh)].append(i)
		else:
			allHash.append(lsh)
			allHashFileID.append([i])

	return files, allHash, allHashFileID, allP

def Normalize(vec):

	res = [0.0] * 12
	s = 0
	for i in vec:
		s += i ** 2
	s = s ** 0.5
	if(s > 0):
		for i in range(12):
			res[i] = float(vec[i]) / s
	return res

def CalcSimilarity(A, B):
	A = Normalize(A)
	B = Normalize(B)
	res = 0.0
	for i in range(12):
		res += A[i] * B[i]
	return res

def Search_LSH(imgurl, files, allHash, allHashFileID, allP,Sub):

	res = []
	p = CalcP(imgurl)
	lsh = CalcLSH(p, Sub)
	if lsh not in allHash:
		return res
	ind = allHash.index(lsh)

	for i in allHashFileID[ind]:
		res.append([files[i].split('.')[0], CalcSimilarity(p, allP[i]), files[i]])
	res.sort(lambda x, y : cmp(x[1], y[1]), reverse = True)
	return res

def Search_backup(imgurl,Sub,allP):

	res = []
	p = CalcP(imgurl)
	files = os.listdir('dataset')
	for i in range(len(files)):
		imgurl = 'dataset/' + files[i]
		res.append([files[i].split('.')[0], CalcSimilarity(p,allP[i]), files[i]])
	res.sort(lambda x,y:cmp(x[1],y[1]),reverse=True)
	return res

def main():

	print 'Program is starting...'

	imgs = []
	imglist = os.listdir('testset')
	for img in imglist:
		imgs.append('testset/' + img)
	Sub = [2,4,9,11,13,21]

	Allcnt = len(imglist)
	passcnt = 0.0
	print 'Update trained data?(Y/N)'
	tmp = raw_input()
	folder = 'Bindata/'
	if tmp == 'Y' or tmp == 'y':
		print 'Initializing...'
		files, allHash, allHashFileID, allP = Initializing(Sub)
		numpy.save(folder + 'files.npy', files)
		numpy.save(folder + 'allHash.npy', allHash)
		numpy.save(folder + 'allHashFileID.npy', allHashFileID)
		numpy.save(folder + 'allP.npy', allP)
		print 'Initialized...'
	else:
		print 'Initializing...'
		files = numpy.load(folder + 'files.npy')
		files = files.tolist()
		allHash = numpy.load(folder + 'allHash.npy')
		allHash = allHash.tolist()
		allHashFileID = numpy.load(folder + 'allHashFileID.npy')
		allHashFileID = allHashFileID.tolist()
		allP = numpy.load(folder + 'allP.npy')
		allP = allP.tolist()
		print 'Initialized...'

	for imgurl in imgs:

		print '\nresult for ', imgurl.split('/')[1]
		res = Search_LSH(imgurl, files, allHash, allHashFileID, allP, Sub)
		
		testing_img = cv2.imread(imgurl)
		
		if len(res) <= 1:
			res += Search_backup(imgurl,Sub,allP)
			res.sort(lambda x, y : cmp(x[1], y[1]), reverse = True)
			# res.sort(lambda x, y : cmp(ss.match(testing_img, cv2.imread(x[1])), ss.match(testing_img, cv2.imread(y[1]))), reverse = True)
		# print len(res)
		# for i in range(len(res)):
		# 	print res[i][2]
		# 	source_img = cv2.imread('dataset/' + res[i][2])
		# 	res[i][1] = ss.match(testing_img, source_img)
		# 	print 'result for ' + imgurl + ' and ' + res[i][2] + ' is  ' + str(res[i][1])
		
		# for i in res:
		# 	print i[0]
		print res[0][0]
		if res[0][0].split('.')[0] == imgurl.split('/')[1].split('.')[0]:
			passcnt += 1

	print 'Ratio =', passcnt / Allcnt * 100, '%'

main()