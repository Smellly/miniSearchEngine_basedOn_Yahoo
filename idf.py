# -*- encoding:utf-8 -*-
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-12-20 09:57:13
# @Author  : Jay Smelly (j.c.xing@qq.com)
# @Link    : None
# @Version : 1.2

__author__ = 'Shen Chen'

import os
try:
    import cPickle as pkl
except:
    import pickle as pkl
from nltk.stem.porter import PorterStemmer # for stemming
from tqdm import tqdm
import math

def stopWords(path = 'stopWord.txt'):
    porter_stemmer = PorterStemmer()
    stopWords = []
    with open(path, 'r') as fin:
        raw = fin.readlines()
    for word in raw:
        stopWords.append(
            porter_stemmer.stem(
                word.strip('\n').lower().decode('utf-8')))
    return stopWords

def getFileList(path):
    fileList = os.listdir(path)
    return fileList

def idf(idfDict, d, stopWords):
    porter_stemmer = PorterStemmer()
    wordSet = set()
    words = d['Content']
    for word in words:
        w = porter_stemmer.stem(word) # already decode utf-8 in htmlProcess
        if w not in stopWords:
            wordSet.add(w.lower())
    for word in wordSet:
        if word in idfDict:
            idfDict[word] += 1
        else:
            idfDict[word] = 1
    fileList = getFileList('./dictionaries')
    total_file = len(fileList)
    for word, times in idfDict.items():
        idfDict[word] = math.log(total_file/(times + 1))
    return idfDict

if __name__ == '__main__':
    idfDict = dict()
    fileList = getFileList('./dictionaries')
    stopWords = stopWords() # 43776
    # stopWords = [] 43936
    for f in tqdm(fileList):
        # print f
        with open(os.path.join('./dictionaries', f), 'r') as fin:
            d = pkl.load(fin)
        idf(idfDict, d, stopWords)
    # not the same path as dictionaries or will occur an error
    with open('idf.pickle', 'w') as fout:
        pkl.dump(idfDict, fout, True)
    print 'len of idfDict:', len(idfDict)
