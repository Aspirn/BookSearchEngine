#!/usr/bin/env python
# -*- coding:utf-8 -*-
INDEX_DIR = "IndexFiles.index"

import sys, os, lucene
import jieba
from java.io import File
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.util import Version
from org.apache.lucene.search.highlight import Highlighter
from org.apache.lucene.search.highlight import InvalidTokenOffsetsException
from org.apache.lucene.search.highlight import QueryScorer
from org.apache.lucene.search.highlight import SimpleFragmenter
from org.apache.lucene.search.highlight import SimpleHTMLFormatter
from org.apache.lucene.search.highlight import SimpleSpanFragmenter
from org.apache.lucene.util import BytesRef
from org.apache.lucene.index import Term
from org.apache.lucene.search import TermQuery
from org.apache.lucene.analysis.core import WhitespaceAnalyzer
from org.apache.lucene.search import BooleanQuery
from org.apache.lucene.search import BooleanClause

"""
This script is loosely based on the Lucene (java implementation) demo class 
org.apache.lucene.demo.SearchFiles.  It will prompt for a search query, then it
will search the Lucene index in the current directory called 'index' for the
search query entered against the 'contents' field.  It will then display the
'path' and 'name' fields for each of the hits it finds in the index.  Note that
search.close() is currently commented out because it causes a stack overflow in
some cases.
"""
def run(searcher, analyzer, command):
        commandsplit = command.split()
        maxlen = len(commandsplit[0])
        maxindex = 0
        for i in range(len(commandsplit)):
            if maxlen < len(commandsplit[i]):
                maxlen = len(commandsplit[i])
                maxindex = i
        commands = " ".join(jieba.cut(command.split()[maxindex])).split()
        querys = BooleanQuery()
        for i in commands:
            try:
                query = QueryParser(Version.LUCENE_CURRENT, "name",
                                analyzer).parse(i)
                querys.add(query, BooleanClause.Occur.MUST)
            except:
                continue
        scoreDocs = searcher.search(querys, 50).scoreDocs
        if len(scoreDocs) == 0:
            querys = BooleanQuery()
            for i in commands:
                for j in i:
                    try:
                        query = QueryParser(Version.LUCENE_CURRENT, "not_seg",
                                        analyzer).parse(j)
                        querys.add(query, BooleanClause.Occur.MUST)
                    except:
                        continue
            scoreDocs = searcher.search(querys, 50).scoreDocs
        temp = []
        if len(scoreDocs) > 0:
            doc = searcher.doc(scoreDocs[0].doc)
            temp = [doc.get("org"), doc.get("path"), doc.get("price"), doc.get("imgsrc")]
        else:
            temp = ['unknown'] * 4
        return temp

def main(title):
    STORE_DIR = "index"
    #lucene.initVM(vmargs=['-Djava.awt.headless=true'])
    #print 'lucene', lucene.VERSION
    #base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    directory = SimpleFSDirectory(File(STORE_DIR))
    searcher = IndexSearcher(DirectoryReader.open(directory))
    analyzer = WhitespaceAnalyzer(Version.LUCENE_CURRENT)
    res = []
    res = run(searcher, analyzer, title)
    del searcher
    return res
