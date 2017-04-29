#!/usr/bin/env python
# encoding=utf-8

import jieba

fs = open("seg_sentence.txt", "w")
jieba.load_userdict("dict.txt")
with open("sentence.txt", "r") as fp:
  for line in fp:
    words = jieba.cut(line)
    sen = ' '.join(words)
    fs.write(sen.encode('utf-8'))
    fs.write('\n')
fs.close()
 
