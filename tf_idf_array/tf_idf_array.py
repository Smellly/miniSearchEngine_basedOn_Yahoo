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


def tf_idf_array():
    # with open('file_word_tf_array/file_word_tf_array.pickle', 'r') as fin:
    #     file_word_tf_array = pkl.load(fin)
    file_word_tf_array = np.load('file_word_tf_array/file_word_tf_array.npy')

    with open('word_idf_array/word_idf_array.pickle', 'r') as fin:
        word_idf_array = pkl.load(fin)

    print 'size of file_word_tf_array: %d * %d'%\
        (len(file_word_tf_array), len(file_word_tf_array[0]))
    print 'size of word_idf_array: %d * %d'%\
        (len(word_idf_array), len(word_idf_array[0]))
    tf_idf_array = file_word_tf_array * word_idf_array
    
   # for index in range(len(file_word_tf_array[3])):
    #    if file_word_tf_array[3][index] != 0:
     #       print file_word_tf_array[3][index]
    for index in range(len(tf_idf_array[1])):
        print tf_idf_array[2][index]

    saveFile('tf_idf_array/tf_idf_array.pickle', tf_idf_array)

if __name__ == '__main__':
    tf_idf_array()
