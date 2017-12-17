# EE208-Teamproject
A search engine based on text and image search for better book searching experience
Team member : Bing Han, Guandong Lu, Yong Mao

## environment
- requirements: tensorflow 1.3, cuda v8.0, cython 0.24, opencv 2.4, easydict
- system: Ubuntu 16.04

## process
- trained on GTX 1070£¬driver version Nvidia 388.59 WHQL
- 50,000 iterations, about 2.5hrs

## note
- book information is crawled from amazon, dangdang and jingdong.
- book names, authors, prices, pictures and comments are extracted from html files
- trained data matrix is stored in VGG_imagenet.npy