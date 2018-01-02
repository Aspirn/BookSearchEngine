#coding:utf-8
import model
from glob import glob
import numpy as np
from PIL import Image
import numpy as np
import time
paths = glob('./test/*.*')

if __name__ =='__main__':
    for i in paths:
        im = Image.open(i)
        img = np.array(im.convert('RGB'))
        t = time.time()
        result,img = model.model(img,model='keras')
        print "It takes time:{}s".format(time.time()-t)
        print "---------------------------------------"
        #Image.fromarray(img).save('/tmp/tmp.jpg')
        print i.split('/')[len(i.split('/')) - 1]
        for key in result:
            print result[key][1]
        #display('/tmp/tmp.jpg')
