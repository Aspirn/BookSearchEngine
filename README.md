# EE208-Teamproject

A search engine based on text and image search for better book searching experience.

Team member : Bing Han, Guandong Lu, Yong Mao

**The following are the main information.For the detail, please see our <a href = "https://github.com/yyong119/EE208-Teamproject/blob/master/Book_search_reporter.pdf"> project reporter</a>**

## File structure
- the web framework is in ft5_40_magazine and ftmp8_41_rs
- crawler, index and search related codes are stored in <i>crawler</i>.
- datum crawled is not included in this repository, more in the <a href = "https://github.com/yyong119/EE208-Teamproject/blob/master/data.png">pic</a>
- image recognition codes are stored in <i>ctpn</i> and <i>get_title_position</i>.Other neural network related files are in <i>checkpoints, crnn, data, img, lib, ocr, prepare_training_data and train</i>

## Setup
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

## Acknowledgements
- the classification part of OCR is forked from <a href = "https://github.com/chineseocr/chinese-ocr">chinese-ocr</a>
- Chinese text segmentation system <a href = "https://github.com/fxsjy/jieba">jieba</a>

## License

This project is licensed under MIT License.

Copyright (c) 2018 Yong Mao, Bing Han, Guandong Lu

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
