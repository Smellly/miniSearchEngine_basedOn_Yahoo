# -*- encoding:utf-8 -*-
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-12-20 09:57:13
# @Author  : Jay Smelly (j.c.xing@qq.com)
# @Link    : None
# @Version : 1.4
__author__ = 'Shen Chen'

import os
import re
try:
    import cPickle as pkl
except:
    import pickle as pkl
from nltk.stem.porter import PorterStemmer # for stemming
from nltk.tokenize import RegexpTokenizer  # for tokenize
from idf import stopWords
from tqdm import tqdm
# from nltk import word_tokenize


def getFileList(path):
    fileList = []
    raw = os.listdir(path)
    for f in raw:
        f = os.path.join('urls', f)
        fileList.append(f)
    return fileList

def loadFile(path):
    html = None
    with open(path, 'r') as fin:
        html = fin.read()
    return html

def saveFile(path, obj):
    with open(path, 'w') as fout:
        pkl.dump(obj, fout, True)

def rePattern():
    r3 = re.compile('[<][\s\S]*?[>]')
    r2 = re.compile('<style[\s\S]*?style>')
    r1 = re.compile('(<script)[\s\S]*?(/script>)')
    return [r1, r2, r3]

# extract title and content
# do word segment and word stemming
# lower all the words
# calculate the word frequency
# return wordDict
# wordDict['Title'] = html.title
# wordDict['Content'] = html.content
def fileProcess(patternList, html_doc, stopWords):
    porter_stemmer = PorterStemmer()
    tokenizer = RegexpTokenizer(r'\w+')
    wordDict = dict()
    url = html_doc.split('\n')[0]
    # remove url from html_doc
    html_doc = html_doc[len(url):] 
    # print url
    wordDict['Url'] = url
    '''
    pattern : 正则中的模式字符串。
    repl : 替换的字符串，也可为一个函数。
    string : 要被查找替换的原始字符串。
    count : 模式匹配后替换的最大次数，默认 0 表示替换所有的匹配。
    '''
    title = re.search('<title.*?title>', html_doc).group()[7:-8]
    # print title
    wordDict['Title'] = title
    for r in patternList:
        html_doc = re.sub(r, ' ', html_doc, count=0)  
    # content = word_tokenize(html_doc.decode('utf8'))
    wordDict['Raw'] = html_doc.decode('utf8')
    content = tokenizer.tokenize(html_doc.decode('utf8'))
    if not content: print title
    wordDict['Content'] = content
    wordDict['Length'] = 0
    for word in content:
        try:
            word_u = porter_stemmer.stem(word.lower())
            # print word_u
            if word_u not in stopWords:
                wordDict['Length'] += 1
                if word_u in wordDict:
                    wordDict[word_u] += 1
                else:
                    wordDict[word_u] = 1
        except:
            print 'can\'t tokenize word:', word

    return wordDict


if __name__ == '__main__':

    # prepere
    patternList = rePattern()
    if not os.path.exists('dictionaries'):
        os.mkdir('dictionaries')

    # run
    fileList = getFileList('urls')
    stopWords = stopWords()
    for f in tqdm(fileList):
        html_doc = loadFile(f)
        wordDict = fileProcess(patternList, html_doc, stopWords)
        savePath = f.replace('urls', 'dictionaries').replace('html', 'pickle')
        saveFile(savePath, wordDict)
