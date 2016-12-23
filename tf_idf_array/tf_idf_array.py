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
    word_idf_array = np.load('word_idf_array/word_idf_array.npy')

    print 'size of file_word_tf_array:', file_word_tf_array.shape
    print 'size of word_idf_array:', word_idf_array.shape
    tf_idf_array = file_word_tf_array * word_idf_array
    print 'size of tf_idf_array:', tf_idf_array.shape
    # saveFile('tf_idf_array/tf_idf_array.pickle', tf_idf_array)
    print 'save to tf_idf_array/tf_idf_array.npy'
    assert(sum(sum(tf_idf_array)) > 0)
    np.save('tf_idf_array/tf_idf_array.npy', tf_idf_array)

if __name__ == '__main__':
    tf_idf_array()
