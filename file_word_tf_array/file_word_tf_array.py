#!/usr/bin/env python
# coding=utf-8

from tqdm import tqdm
import numpy as np
try:
    import cPickle as pkl
except:
    import pickle as pkl

def saveFile(path, obj):
    with open(path, 'w') as fout:
        pkl.dump(obj, fout, True)


def file_word_tf_array():
    with open('word_file_index/file_index.pickle', 'r') as fin:
        file_index = pkl.load(fin)
    with open('word_file_index/word_index.pickle', 'r') as fin:
        word_index = pkl.load(fin)

    file_word_tf_array = list()
    l = len(file_index)
    for index_file in tqdm(range(l)):
        file_word_tf_array.append([])
        with open('dictionaries/'+file_index[index_file], 'r') as fin:
            file_dict = pkl.load(fin)
            for index_word in range(len(word_index)):
                if word_index[index_word] in file_dict:
                    # log way
                    # tf = np.log(file_dict[word_index[index_word]]) + 1
                    # Term Frequancy way
                    tf = float(file_dict[word_index[index_word]])/file_dict['Length']
                    file_word_tf_array[index_file].append(tf)
                else:
                    file_word_tf_array[index_file].append(0)

    file_word_tf_array = np.array(file_word_tf_array)

    # saveFile('file_word_tf_array/file_word_tf_array.pickle', file_word_tf_array)
    print 'save to file_word_tf_array/file_word_tf_array.npy'
    np.save('file_word_tf_array/file_word_tf_array.npy', file_word_tf_array)


if __name__ == '__main__':
    file_word_tf_array()
