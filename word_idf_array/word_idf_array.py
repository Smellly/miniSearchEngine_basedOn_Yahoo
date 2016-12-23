#!/usr/bin/env python
# coding=utf-8
import numpy as np
try:
    import cPickle as pkl
except:
    import pickle as pkl

def saveFile(path, obj):
    with open(path, 'w') as fout:
        pkl.dump(obj, fout, True)

def word_idf_array():
    with open('idf.pickle', 'r') as fin:
        word_idf = pkl.load(fin)
    with open('word_file_index/word_index.pickle', 'r') as fin:
        word_index = pkl.load(fin)

    word_idf_array = list()
    for index in range(len(word_index)):
        print index, word_index[index], word_idf[word_index[index]]
        word_idf_array.append(word_idf[word_index[index]])

    word_idf_array = np.array(word_idf_array)

    # saveFile('word_idf_array/word_idf_array.pickle', word_idf_array)
    print 'save to word_idf_array/word_idf_array.npy'
    np.save('word_idf_array/word_idf_array.npy', word_idf_array)
    
   # for index in range(len(word_idf)):
    #    print index, word_index[index],word_idf[word_index[index]], word_idf_array[index]

if __name__ == '__main__':
    word_idf_array()
