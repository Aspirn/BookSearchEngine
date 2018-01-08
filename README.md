# EE208-Teamproject
A search engine based on text and image search for better book searching experience
Team member : Bing Han, Guandong Lu, Yong Mao

## setup
- requirements: tensorflow 1.4, cuda v8.0, cython 0.24, opencv 2.4, easydict, keras 2.0.8, pytorch v0.1.12
- system: Ubuntu 16.04
- build the library
```shell
cd EE2.8-Teamproject/
sh setup.sh
cd lib/utils
chmod +x make.sh
./make.sh
```

## process
- trained on GTX 1070��driver version Nvidia 388.59 WHQL(from Nvidia-smi)
- 50,000 iterations, about 2.5hrs

## note
- book information is crawled from amazon, dangdang and jingdong.
- comment information is gotten from douban.
- we are connected to SJTU library to know whether it can be borrowed.

## structure
- crawler and index related codes are stored in <i>crawler</i>.
- datum crawled is not included in this repository
- image recognition codes are stored in <i>ctpn</i>(lsh and sift and some other stuff is not related to ctpn. It's just for conveniance to put them all in it).Other neural network related files are in <i>checkpoints, crnn, data, img, lib, ocr, prepare_training_data and train</i>

## acknowledgements
- the classification part of OCR is forked from <a href = "https://github.com/chineseocr/chinese-ocr">chinese-ocr</a>
