# -*- coding: utf-8 -*-


import numpy
import os
try:
    import cPickle as pkl
except:
    import pickle as pkl


def saveFile(path, obj):
    with open(path, 'w') as fout:
        pkl.dump(obj, fout, True)


def word_file_index():
    path = os.listdir('dictionaries')
    file_index = dict()
    index = 0
    #为每份文档建立一个ID编码
    for file in path:   
        file_index[index] = file
        index = index + 1

    word_index = dict()
    index = 0
    # 为每个单词建立一个ID编码
    with open('idf.pickle', 'r') as fin:  
        d = pkl.load(fin)
        # del d['Url']
        # del d['Title']
        # del d['Content']
        # del d['Raw']
        for word, idf in d.items():
            # if word != 'Url' and word != 'Title' and word != 'Content' and word != 'Raw':
            # idf.pickle 中沒有存 url title相關信息
            # print word
            word_index[index] = word
            index = index + 1

    # 文件編碼
    print 'save to word_file_index/file_index.pickle'
    saveFile('word_file_index/file_index.pickle', file_index) 
    # 單詞編碼
    print 'save to word_file_index/word_index.pickle'
    saveFile('word_file_index/word_index.pickle', word_index)


if __name__ == "__main__":
    word_file_index()
