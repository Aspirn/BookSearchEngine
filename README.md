# EE208-Teamproject

A search engine based on text and image search for better book searching experience.

Team member : Bing Han, Guandong Lu, Yong Mao

**The following are the main information.For the detail, please see our <a href = "https://github.com/yyong119/EE208-Teamproject/blob/master/Book_search_reporter.pdf"> project reporter</a>**

## file structure
- the web framework is in ft5_40_magazine and ftmp8_41_rs
- crawler, index and search related codes are stored in <i>crawler</i>.
- datum crawled is not included in this repository, more in the <a href = "https://github.com/yyong119/EE208-Teamproject/blob/master/data.png">pic</a>
- image recognition codes are stored in <i>ctpn</i> and <i>get_title_position</i>.Other neural network related files are in <i>checkpoints, crnn, data, img, lib, ocr, prepare_training_data and train</i>

## setup
- requirements: tensorflow 1.4, cuda v8.0, cython 0.24, opencv 2.4, easydict, keras 2.0.8, pytorch v0.1.12
- system: Ubuntu 16.04
- build the library(sudo is recommended)
```shell
cd EE208-Teamproject/
sh setup.sh
cd lib/utils
chmod +x make.sh
./make.sh
```
- run mysite.py and browse localhost:8080

## Connectionist Text Proposal Network train process
- trained on GTX 1070��driver version Nvidia 388.59 WHQL(from Nvidia-smi)
- 50, 000 iterations, about 2.5hrs

## acknowledgements
- the classification part of OCR is forked from <a href = "https://github.com/chineseocr/chinese-ocr">chinese-ocr</a>
- Chinese text segmentation system <a href = "https://github.com/fxsjy/jieba">jieba</a>
