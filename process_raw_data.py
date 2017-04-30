#!/usr/bin/python
# encoding=utf-8

import re
import jieba

fs = open("train-data.txt", "w")
fw = open("dict2.txt", "w")

dict = {}
tags = {}

def addToDict(w):
  if w in dict:
    dict[w] += 1
  else:
    dict[w] = 1

def addToTag(w):
  if w in tags:
    tags[w] += 1
  else:
    tags[w] = 1

with open("raw_marked_data.txt", "r") as fp:
  sentence = ''
  seg_list = []
  line_num = 0
  sent_num = 0
  for line in fp:
    line_num += 1
    if len(line) == 1:
      seged_list = []
      processed_list = []
      test_sen = ''
      parts = []
      token_dict = {}
      for s in seg_list:
        mo = re.search('\{(.*)\}:\{(.*)\}', s)
        entities = mo.group(1).split(',')
        states = mo.group(2).split(',')
        for e in entities:
          if e == 'null':
            continue
          emo = re.search('(.*)\[(.*)\]', e)
          addToDict(emo.group(1))
          addToTag(emo.group(2))
          parts.append(emo.group(1))
          token_dict[emo.group(1)] = emo.group(2)
        for s in states:
          smo = re.search('(.*)\[(.*)\]', s)
          addToDict(smo.group(1))
          addToTag(smo.group(2))
          parts.append(smo.group(1))
          token_dict[smo.group(1)] = smo.group(2)

      print sentence
      for key in token_dict:
        print ("%s\t%s" % (key, token_dict[key]))
      for ppp in parts:
        jieba.add_word(ppp, 10000000)
      seg_s = jieba.cut(sentence, HMM=False)
      token_id = 0
      for sss in seg_s:
        tag = 'None'
        if sss in token_dict:
          tag = token_dict[sss]
        
        sss = sss.encode('utf-8')
        if tag == 'None':
          if sss in token_dict:
            tag = token_dict[sss]
        print type(sss)
        print type(tag)
        print sss
        print tag
        token_id += 1
        new_parts = []
        new_parts.append(str(token_id)) # f0
        new_parts.append(sss)      # f1
        new_parts.append('_')      # f2
        new_parts.append(tag)      # f3
        new_parts.append('_')      # f4
        new_parts.append('_')      # f5
        new_parts.append('_')      # f6
        new_parts.append('_')      # f7
        new_parts.append('_')      # f8
        new_parts.append('SpaceAfter=No') # f9
        processed_list.append(new_parts)
      
      # assert sentence == test_sen
      fs.write('# sent_id = %d\n' % sent_num)
      sent_num += 1
      fs.write('# text = ')
      fs.write(sentence)
      fs.write('\n')
      for np in processed_list:
        fs.write('\t'.join(np))
        fs.write('\n')
      fs.write('\n')
      sentence = ''
      seg_list = []

    elif not line.startswith("{"):
      sentence = line[:-1]
    else:
      seg_list.append(line);


fs.close()
for key in dict:
  fw.write(key)
  fw.write(' ')
  fw.write(str(dict[key]))
  fw.write('\n')
fw.close 

for key in tags:
  print ("%s:%d" %(key, tags[key]))

