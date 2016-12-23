#!/usr/bin/env python
# coding=utf-8

import time
from tqdm import tqdm
try:
    import cPickle as pkl
except:
    import pickle as pkl


#返回单词word在文件file_path中首次出现的起止位置
# file_path为dictionaries目录下的某个文件
def word_location(word, file_path):
    with open(file_path, 'r') as fin:
        file_dict = pkl.load(fin)
    content = file_dict['Raw']
    pos_start = content.find(word)
    pos_end = pos_start + len(word) - 1
    return pos_start, pos_end

def saveFile(path, obj):
    with open(path, 'w') as fout:
        pkl.dump(obj, fout, True)

#inverted_list数据结构为python下的一个字典, 字典的key为每个单词,对应的value
#为一个list,list每个元素为一个子list，子list结构为[文档ID, key的起始位置, key的结束位置]
def inverted_list():
    inverted_list = dict()
    with open('word_file_index/file_index.pickle', 'r') as fin:
        file_index = pkl.load(fin)
    with open('word_file_index/word_index.pickle', 'r') as fin:
        word_index = pkl.load(fin)

    start = time.time()
    l = len(word_index)
    for index_word in tqdm(range(l)):
        inverted_list[word_index[index_word]] = []
        index = 0
        for index_file in range(len(file_index)):
          #  print file_index[index_file]
            pos_start, pos_end = word_location(
                word_index[index_word],
                'dictionaries/'+ file_index[index_file])
            if pos_start != -1:
                inverted_list[word_index[index_word]].append([])
                inverted_list[word_index[index_word]][index].append(index_file)
                inverted_list[word_index[index_word]][index].append(pos_start)
                inverted_list[word_index[index_word]][index].append(pos_end)
                index = index + 1
            else:
                pass
                # print index_word, word_index[index_word], index_file, file_index[index_file]
    end = time.time()
    consume_time = end - start
    consume_time = time.strftime('%H:%M:%S', time.gmtime(consume_time))
    print '---------------------', consume_time, '-------------------------'
    saveFile('inverted_list/inverted_list.pickle', inverted_list)

if __name__ == '__main__':
    inverted_list()
