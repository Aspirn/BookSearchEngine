# -*- coding:utf-8 -*-
'''
from ctpn.test import find_bbox as fb
然后使用只需要fb(图片的url)即可返回识别到的文字
'''
from __future__ import print_function
import tensorflow as tf
import numpy
import os, sys, cv2
import glob
import shutil
sys.path.append(os.getcwd())
from lib.networks.factory import get_network
from lib.fast_rcnn.config import cfg,cfg_from_file
from lib.fast_rcnn.test import test_ctpn
from lib.utils.timer import Timer
from lib.text_connector.detectors import TextDetector
from lib.text_connector.text_connect_cfg import Config as TextLineCfg
import json
from aip import AipOcr
import os

def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()


def resize_im(im, scale, max_scale = None):
    f = float(scale) / min(im.shape[0], im.shape[1])
    if max_scale != None and f * max(im.shape[0], im.shape[1]) > max_scale:
        f = float(max_scale) / max(im.shape[0], im.shape[1])
    return cv2.resize(im, None, None, fx = f, fy = f, interpolation = cv2.INTER_LINEAR), f

def draw_boxes(img, image_name, boxes, scale):
    res = []
    res2 = []
    final = []
    tmp = 0
    tmp2 = 0
    for box in boxes:
        # print(box[0], box[1], box[2], box[3], box[4], box[5], box[6], box[7])
        if box[5] - box[1] > tmp:
            tmp = box[5] - box[1]
            res = box
    for box in boxes:
        # print(box[0], box[1], box[2], box[3], box[4], box[5], box[6], box[7])
        if box[5] - box[1] > tmp2 and box[5] != res[5]:
            tmp2 = box[5] - box[1]
            res2 = box
    final.append(res)
    final.append(res2)
    color1 = (0, 255, 0)
    color2 = (0, 0, 255)
    # cv2.line(img, (int(res[0]), int(res[1])), (int(res[2]), int(res[3])), color1, 2)
    # cv2.line(img, (int(res[0]), int(res[1])), (int(res[4]), int(res[5])), color1, 2)
    # cv2.line(img, (int(res[6]), int(res[7])), (int(res[2]), int(res[3])), color1, 2)
    # cv2.line(img, (int(res[4]), int(res[5])), (int(res[6]), int(res[7])), color1, 2)
    # cv2.line(img, (int(res2[0]), int(res2[1])), (int(res2[2]), int(res2[3])), color1, 2)
    # cv2.line(img, (int(res2[0]), int(res2[1])), (int(res2[4]), int(res2[5])), color2, 2)
    # cv2.line(img, (int(res2[6]), int(res2[7])), (int(res2[2]), int(res2[3])), color2, 2)
    # cv2.line(img, (int(res2[4]), int(res2[5])), (int(res2[6]), int(res2[7])), color2, 2)
    base_name = image_name.split('/')[-1]
    # img = cv2.resize(img, None, None, fx = 1.0 / scale, fy = 1.0 / scale, interpolation = cv2.INTER_LINEAR)
    cv2.imwrite(os.path.join("data/results", base_name), img)
    img2 = img[int(res[1]) : int(res[5]), int(res[0]) : int(res[2])]
    cv2.imwrite(os.path.join("data/results", 'test1.png'), img2)  
    img3 = img[int(res2[1]) : int(res2[5]), int(res2[0]) : int(res2[2])]
    cv2.imwrite(os.path.join("data/results", 'test2.png'), img3)     
    return final

def ctpn(sess, net, image_name):
    timer = Timer()
    timer.tic()

    img = cv2.imread(image_name)
    img, scale = resize_im(img, scale = TextLineCfg.SCALE, max_scale = TextLineCfg.MAX_SCALE)
    scores, boxes = test_ctpn(sess, net, img)

    textdetector = TextDetector()
    boxes = textdetector.detect(boxes, scores[ : , numpy.newaxis], img.shape[:2])
    draw_boxes(img, image_name, boxes, scale)
    timer.toc()
    print(('Detection took {:.3f}s for '
           '{:d} object proposals').format(timer.total_time, boxes.shape[0]))



def find_bbox(url):
# if __name__ == '__main__':


    # im_names = glob.glob(os.path.join(cfg.DATA_DIR, 'demo', '*.png')) + \
    #            glob.glob(os.path.join(cfg.DATA_DIR, 'demo', '*.jpg')) + \
    #            glob.glob(os.path.join(cfg.DATA_DIR, 'demo', '*.PNG')) + \
    #            glob.glob(os.path.join(cfg.DATA_DIR, 'demo', '*.JPG'))

    # for im_name in im_names:
    #     print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    #     print(('Demo for {:s}'.format(im_name)))
    #     print(im_name)
    #     ctpn(sess, net, im_name)
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    print('Demo for ', url)
    ctpn(sess, net, url)  


    image = get_file_content(os.getcwd() + '/data/results/test1.png')
    image2 = get_file_content(os.getcwd() + '/data/results/test2.png')


    APP_ID = '10634722'
    API_KEY = '9T9pkzckvioQ9pocGHLPnaBd'
    SECRET_KEY = 'ULMstHiUUKRRheOGrBnZRi5DjGHtVNzx'

    client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

    options = {}
    options["language_type"] = "CHN_ENG"
    options["detect_direction"] = "true"
    options["detect_language"] = "true"
    options["probability"] = "true"

    print('###', client.basicGeneral(image, options))
    try:
        return client.basicGeneral(image, options)['words_result'][0]['words'].encode('utf-8') + client.basicGeneral(image2, options)['words_result'][0]['words'].encode('utf-8')
    except:
        try:
            return client.basicGeneral(image, options)['words_result'][0]['words'].encode('utf-8')
        except:
            return client.basicGeneral(image2, options)['words_result'][0]['words'].encode('utf-8')

if os.path.exists("results/"):
    shutil.rmtree("results/")
os.makedirs("results/")

cfg_from_file('ctpn/text.yml')

# init session
config = tf.ConfigProto(allow_soft_placement = True)
sess = tf.Session(config = config)
# load network
net = get_network("VGGnet_test")
# load model
print(('Loading network {:s}... '.format("VGGnet_test")), end = ' ')
saver = tf.train.Saver()

try:
    ckpt = tf.train.get_checkpoint_state(cfg.TEST.checkpoints_path)
    print('Restoring from {}...'.format(ckpt.model_checkpoint_path), end = ' ')
    saver.restore(sess, ckpt.model_checkpoint_path)
    print('done')
except:
    raise 'Check your pretrained {:s}'.format(ckpt.model_checkpoint_path)

im = 128 * numpy.ones((300, 300, 3), dtype = numpy.uint8)
for i in range(2):
    _, _ = test_ctpn(sess, net, im)

# url = raw_input()
# url = os.path.join(url)
# print(url)
# find_bbox(url)





### {u'log_id': 3877553716130621000, u'direction': 0, u'words_result_num': 1, u'words_result': [{u'words': u'\u5b66\u7269\u7406', u'probability': {u'variance': 1e-06, u'average': 0.998848, u'min': 0.997186}}], u'language': -1}
### {u'log_id': 1071110066153489474, u'direction': 0, u'words_result_num': 1, u'words_result': [{u'probability': {u'variance': 2.1e-05, u'average': 0.99758, u'min': 0.987327}, u'words': u'\u5927\u5b66\u7269\u7406\u6559\u7a0b'}], u'language': 3}


[{u'words': u'\u5b66\u7269\u7406', u'probability': {u'variance': 1e-06, u'average': 0.998848, u'min': 0.997186}}]
[{u'probability': {u'variance': 2.1e-05, u'average': 0.99758, u'min': 0.987327}, u'words': u'\u5927\u5b66\u7269\u7406\u6559\u7a0b'}]
