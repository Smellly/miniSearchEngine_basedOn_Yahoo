#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-12-23 15:49:13
# @Author  : Jay Smelly (j.c.xing@qq.com)
# @Link    : None
# @Version : 1.3

import time
import sys
import numpy as np
from nltk.stem.porter import PorterStemmer # for stemming
from nltk.tokenize import RegexpTokenizer  # for tokenize
try:
    import cPickle as pkl
except:
    import pickle as pkl

# 計算兩個 tf-idf 的歐幾里得距離
#　越小越接近
# w1,w2 is a np.array()
def euclideanDistance(w1, w2):
    res = np.square(w1 - w2)
    ans = np.sqrt(np.sum(res))
    return ans

# 計算兩個 tf-idf 的餘弦距離
# 越大越接近
# w1,w2 is a np.array()
def cosineDistance(w1, w2):
    numerator = np.sum(w1 * w2)
    denominator = np.sqrt(np.sum(np.square(w1)) * np.sum(np.square(w2)))
    return float(numerator)/denominator                                                                                                                                                                                                                                                                                                                                                                                                        

def words2tfidf(query_word_list):
    # log(M/DFi)
    with open('idf.pickle') as fin:
        idf = pkl.load(fin)
    qTfidf = np.zeros(len(idf))
    for keyword in query_word_list:
        if keyword not in idf:
            continue
        index = idf.keys().index(keyword)
        assert(index != -1)
        qTfidf[index] = idf[keyword]
    assert(sum(qTfidf) > 0)
    return qTfidf

# input:
# str
# output:
# k nearest_file_id
def query(query_word_list, K = 20):
    with open('word_file_index/file_index.pickle', 'r') as fin:
        file_index = pkl.load(fin)
    # print 'loading inverted_list/inverted_list_test.pickle'
    with open('inverted_list/inverted_list_test.pickle', 'r') as fin:
        inverted_list = pkl.load(fin)
    tf_idf_array = np.load('tf_idf_array/tf_idf_array.npy')

    query_tfidf = words2tfidf(query_word_list)
    
    # fetch relevant articles from inverted list
    articles = set()
    fileIDict = dict() 
    # value is [[keyword1index, (start_pos1, end_pos1)]
    #        ,[keyword2index, (start_pos2, end_pos2)], ...]
    for keyword in query_word_list:
        if keyword in inverted_list:
            # print keyword, 'in our data'
            tmp = inverted_list[keyword]
            for t in tmp:
                # save start_pos and end_pos
                if t[0] in fileIDict:
                    fileIDict[t[0]].append([keyword, (t[1], t[2])])
                else:
                    fileIDict[t[0]] = [[keyword, (t[1], t[2])]]
                # compute distance
                # print 'sum query_tfidf :', sum(query_tfidf)
                # print 'sum tf_idf_array:', sum(tf_idf_array[t[0]])
                d_cos = cosineDistance(query_tfidf, tf_idf_array[t[0]])
                # d_eu = euclideanDistance(query_tfidf, tf_idf_array[t[0]])
                # print 'cosine    distance:', d
                # print 'euclidean distance:', d2
                articles.add((t[0], d_cos))
        else:
            # print keyword, 'NOT in our data'
            pass

    articles  = sorted(list(articles)[:K], key =lambda x:x[1], reverse = True) # d_cos
    # articles.sort(key =lambda x:x[1], reverse = False) # d_eu
    res = []
    # print 'after sort:', articles[:20]
    for file_id, dis in articles:
        articleList = fileIDict[file_id]
        file_idList = [x[0] for x in articleList]
        # print file_id, articleList, file_idList
        tmp = [file_id]
        for keyword in query_word_list:
            try:
                idx = file_idList.index(keyword)
                # print '\t', keyword, articleList[file_idList.index(keyword)]
                tmp.append(articleList[idx][1])
            except:
                tmp.append((-1, -1))
        res.append(tmp)
    return res

def preprocess():
    porter_stemmer = PorterStemmer()
    tokenizer = RegexpTokenizer(r'\w+')
    sents = []
    for i in range(1, len(sys.argv)):
        try:
            tmp = tokenizer.tokenize(sys.argv[i].decode('utf8'))
        except:
            tmp = tokenizer.tokenize(sys.argv[i])
        for word in tmp:
            word = porter_stemmer.stem(word.lower())
            sents.append(word)
    # print sents
    return sents

if __name__ == '__main__':

    # input is a string
    # start = time.time()
    sents = preprocess()
    res =  query(sents)
    # end = time.time()
    # for i in res:
    #     print i
    # consume_time = end - start
    # print '---------------------', consume_time, '-------------------------'
