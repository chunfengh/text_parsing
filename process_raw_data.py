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

class Token:
  def __init__(self, word, tag):
    self.word = word
    self.tag = tag
    self.parent = None
    self.r = ''
    self.id = 0
  def __eq__(self, other):
    if isinstance(other, self.__class__):
      return self.word == other.word and self.tag == other.tag
    return False;
  def __ne__(self, other):
    return not self.__eq__(other)
  def __str__(self):
    return 'Word:%s, Tag:%s, Parent:%s, Relation:%s, Id:%d' % (self.word, self.tag, self.parent, self.r, self.id)


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
      token_dict = {}
      tokens = []
      for s in seg_list:
        mo = re.search('\{(.*)\}:\{(.*)\}', s)
        entities = mo.group(1).split(',')
        states = mo.group(2).split(',')
        et = []
        ept = None
        for e in entities:
          if e == 'null':
            continue
          emo = re.search('(.*)\[(.*)\]', e)
          addToDict(emo.group(1))
          addToTag(emo.group(2))
          token = Token(emo.group(1), emo.group(2))
          et.append(token)
          if token.tag == '实体':
            ept = token
        dup_e = True 
        et2 = []
        for t in et:
          if t.word not in token_dict:
            token_dict[t.word] = t
            dup_e = False
            et2.append(t)
          else:
            et2.append(token_dict[t.word])
        if not dup_e:
          for t in et2:
            if t != ept:
              t.parent = ept
              if t.tag == '前置位置':
                t.r = 'pre_pos'
              elif t.tag == '后置位置':
                t.r = 'post_pos'
        else:
          ept = None

        st = []
        spt = None
        for s in states:
          smo = re.search('(.*)\[(.*)\]', s)
          addToDict(smo.group(1))
          addToTag(smo.group(2))
          token = Token(smo.group(1), smo.group(2))
          token_dict[token.word] = token
          st.append(token)
          if token.tag == '异常' or token.tag == '疾病':
            spt = token
        for t in st:
          if t != spt:
            t.parent = spt
          if t.tag == '程度':
             t.r = 'degree'
          elif t.tag == '异常性质':
             t.r = 'property'
          elif t.tag == '比较属性':
             t.r = 'compare'
          elif t.tag == '治疗相关属性':
             t.r = 'operate'

        if ept:
          ept.parent = spt
          ept.r = 'illness'
        elif spt:
          # Loop back to first root, set as parent with relation and
          for tt in reversed(tokens):
            if not tt.parent:
              spt.parent = tt
              spt.r = 'and'
              break

        tokens = tokens + st
        if not dup_e:
          tokens = tokens + et2

      print sentence
      for t in tokens:
        jieba.add_word(t.word, 10000000)
      seg_s = jieba.cut(sentence, HMM=False)
      token_id = 0
      seg_ss = []
      for sss in seg_s:
        token_id += 1
        seg_ss.append(sss)
        if sss in token_dict:
          token_dict[sss].id = token_id
        else:
          sss = sss.encode('utf-8')
          if sss in token_dict:
            token_dict[sss].id = token_id

      token_id = 0
      for key in token_dict:
        print type(key)
        print ("%s\t%s" %(key, token_dict[key])) 
      
      for sss in seg_ss:
        token = None
        if sss in token_dict:
          token = token_dict[sss]
        sss = sss.encode('utf-8')
        if token == None:
          if sss in token_dict:
            token = token_dict[sss]
        print type(sss)
        print type(token)
        print sss
        print token
        token_id += 1
        new_parts = []
        new_parts.append(str(token_id)) # f0
        new_parts.append(sss)      # f1
        new_parts.append('_')      # f2
        new_parts.append(token.tag if token else 'None')      # f3
        new_parts.append(token.tag if token else 'None')      # f4
        new_parts.append('_')      # f5
        new_parts.append(str(token.parent.id) if token and token.parent else '0')      # f6
        new_parts.append(token.r if token else '_')      # f7
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

