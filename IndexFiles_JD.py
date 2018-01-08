#!/usr/bin/env python
# -*- coding:utf-8 -*-
INDEX_DIR = "IndexFiles.index"

import sys, os, lucene, threading, time
from datetime import datetime
from bs4 import BeautifulSoup
import jieba
from java.io import File
from org.apache.lucene.analysis.miscellaneous import LimitTokenCountAnalyzer
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field, FieldType
from org.apache.lucene.index import FieldInfo, IndexWriter, IndexWriterConfig
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.util import Version
from org.apache.lucene.analysis.core import WhitespaceAnalyzer

"""
This class is loosely based on the Lucene (java implementation) demo class 
org.apache.lucene.demo.IndexFiles.  It will take a directory as an argument
and will index all of the files in that directory and downward recursively.
It will index on the file path, the file name and the file contents.  The
resulting Lucene index will be placed in the current directory and called
'index'.
"""

class Ticker(object):

    def __init__(self):
        self.tick = True

    def run(self):
        while self.tick:
            sys.stdout.write('.')
            sys.stdout.flush()
            time.sleep(1.0)

class IndexFiles(object):
    """Usage: python IndexFiles <doc_directory>"""

    def __init__(self, root, storeDir, analyzer, p):

        if not os.path.exists(storeDir):
            os.mkdir(storeDir)

        store = SimpleFSDirectory(File(storeDir))
        analyzer = LimitTokenCountAnalyzer(analyzer, 1048576)
        config = IndexWriterConfig(Version.LUCENE_CURRENT, analyzer)
        config.setOpenMode(IndexWriterConfig.OpenMode.CREATE)
        writer = IndexWriter(store, config)

        self.indexDocs(root, writer, p)
        ticker = Ticker()
        print 'commit index',
        threading.Thread(target=ticker.run).start()
        writer.commit()
        writer.close()
        ticker.tick = False
        print 'done'

    def indexDocs(self, root, writer, p):

        t1 = FieldType()
        t1.setIndexed(True)
        t1.setStored(True)
        t1.setTokenized(False)
        t1.setIndexOptions(FieldInfo.IndexOptions.DOCS_AND_FREQS)
        
        t2 = FieldType()
        t2.setIndexed(True)
        t2.setStored(True)
        t2.setTokenized(True)
        t2.setIndexOptions(FieldInfo.IndexOptions.DOCS_AND_FREQS_AND_POSITIONS)
        filelist = ["result.txt", "result1.txt", "result2.txt", "result3.txt"]
        dic = {}
        for f in filelist:
	        file0 = open(f, 'r')
	        name = ""
	        lock = False
	        endjudge = False
	        line13 = False
	        a = 1
	        for lines in file0.readlines():
	        	try:
		            if lock == False:
	                        name = lines.strip()
	                        dic[name] = []
	                        a = 1
	                        lock = True
	                        endjudge = False
	                        line13 = False
	                    else:
	                        a = a + 1
	                        if a == 3: #type
	                            templist = lines.strip().split(",")
	                            for i in range(len(templist)):
	                                templist[i] = templist[i][1:-1]
	                            dic[name].append(" ".join(templist))
	                        elif a == 4: #price
	                            dic[name].append(lines.strip().split(",")[0][2:-1])
	                        elif a == 5: #src
	                            dic[name].append(lines.strip())
	                        elif a == 6: #comment
	                            lines = unicode(lines, "utf-8")
	                            res = []
	                            templist = lines.strip().split(",")
	                            for item in templist:
	                                if "[['" in item:
	                                    res.append(item[4:-2])
	                            dic[name].append(" ".join(res))
	                        elif a == 12: #ISBN
	                            try:
	                                dic[name].append(str(int(lines.strip()[11:24])))
	                            except:
	                                try:
	                                    dic[name].append(str(int(lines.strip()[11:21])))
	                                except:
	                                    line13 = True
	                        elif a == 13 and line13:
	                            try:
	                                dic[name].append(str(int(lines.strip()[11:24])))
	                            except:
	                                dic[name].append(str(int(lines.strip()[11:21])))
                                elif a == 14 and line13 == False:
                                    dic[name].append(lines.strip()[11:19])
                                elif a == 15 and line13 == True:
                                    dic[name].append(lines.strip()[11:19])
	                        elif a > 12 and lines.strip() == "</ul>":
	                            endjudge = True
	                        elif endjudge and lines.strip() == "":
	                            lock = False
		        except:
		        	continue
    	for n, k in dic.items():
                print "adding", n
                try:
                    doc = Document()
                    n = unicode(n, "utf-8")
                    l = ""
                    for i in n:
                        l = l + i + " "
                    j = " ".join(jieba.cut(n))
                    cuted = " ".join(jieba.cut(k[3]))
                    if p == 1:
                        doc.add(Field("name", j, t2))
                        doc.add(Field("type", k[0], t2))
                        doc.add(Field("price", k[1], t1))
                        doc.add(Field("imgsrc", k[2], t1))
                        doc.add(Field("comment", cuted, t2))
                        doc.add(Field("comment_notseg", "\n".join(k[3].split()), t1))
                        doc.add(Field("ISBN", k[4], t1))
                        doc.add(Field("not_seg", l, t2))
                        doc.add(Field("org", n, t1))
                        doc.add(Field("ID", k[5], t1))
                    writer.addDocument(doc)
                except Exception, e:
                    print "Failed in indexDocs:", e
if __name__ == '__main__':
    """
    if len(sys.argv) < 2:
        print IndexFiles.__doc__
        sys.exit(1)
    """
    lucene.initVM(vmargs=['-Djava.awt.headless=true'])
    print 'lucene', lucene.VERSION
    start = datetime.now()
    try:
        """
        base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
        IndexFiles(sys.argv[1], os.path.join(base_dir, INDEX_DIR),
                   StandardAnalyzer(Version.LUCENE_CURRENT))
                   """
        analyzer = WhitespaceAnalyzer(Version.LUCENE_CURRENT)
        IndexFiles('html', "index1", analyzer, 1)
        end = datetime.now()
        print end - start
    except Exception, e:
        print "Failed: ", e
        raise e
