#!/usr/bin/env python
# -*- coding:utf-8 -*-
INDEX_DIR = "IndexFiles.index"

import SearchFiles
import sys, os, lucene, math
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
def run(searcher, analyzer,command):
        print "\nSearching for: " + command
        # command = unicode(command, 'UTF-8')
        if command == '':
            return
        commands = " ".join(jieba.cut(command)).split()
        commands_notseg = command.split()
        querys = BooleanQuery()
        querys1 = BooleanQuery()
        querys2 = BooleanQuery()
        for i in commands:
            query = QueryParser(Version.LUCENE_CURRENT, "name",
                            analyzer).parse(i)
            querys.setBoost(math.sqrt(len(i)))
            querys.add(query, BooleanClause.Occur.MUST)
            querys1.add(query, BooleanClause.Occur.SHOULD)
        scoreDocs = searcher.search(querys, 50).scoreDocs
        if len(scoreDocs) == 0:
            querys = BooleanQuery()
            for i in commands:
                for j in i:
                    query = QueryParser(Version.LUCENE_CURRENT, "not_seg",
                                    analyzer).parse(j)
                    querys.add(query, BooleanClause.Occur.MUST)
                    querys1.add(query, BooleanClause.Occur.SHOULD)
            scoreDocs = searcher.search(querys, 50).scoreDocs
        for i in commands:
        	query = QueryParser(Version.LUCENE_CURRENT, "comment",
                            		analyzer).parse(i)
        	query.setBoost(0.5)
        	querys2.add(query, BooleanClause.Occur.SHOULD)
        if len(commands) > 1:
            querys2.add(querys1, BooleanClause.Occur.MUST)
        querys2.add(querys, BooleanClause.Occur.SHOULD)
        querys = BooleanQuery()
        for i in commands_notseg:
        	query = QueryParser(Version.LUCENE_CURRENT, "type",
                            analyzer).parse(i)
        	query.setBoost(1.1)
        	querys.add(query, BooleanClause.Occur.SHOULD)
        	
        if len(commands_notseg) > 1:
            querys.add(querys1, BooleanClause.Occur.MUST)
        querys2.add(querys, BooleanClause.Occur.SHOULD)
        scoreDocs = searcher.search(querys2, 20).scoreDocs
        print "%s total matching documents." % len(scoreDocs)
        res = []
        temp = []
        for scoreDoc in scoreDocs:
            doc = searcher.doc(scoreDoc.doc)
            temp = [doc.get("org"), doc.get("type"), doc.get("price"), doc.get("imgsrc"), doc.get('comment_notseg'), doc.get('ISBN'), doc.get('ID')]
            for i in SearchFiles.main(doc.get("org")):
                temp.append(i)
            res.append(temp)
        return res

def main(title):
    STORE_DIR = "index1"
    lucene.initVM(vmargs=['-Djava.awt.headless=true'])
    print 'lucene', lucene.VERSION
    #base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    directory = SimpleFSDirectory(File(STORE_DIR))
    searcher = IndexSearcher(DirectoryReader.open(directory))
    analyzer = WhitespaceAnalyzer(Version.LUCENE_CURRENT)
    res = []
    res = run(searcher, analyzer,title)
    del searcher
    return res

print main("算法导论")
