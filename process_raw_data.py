#!/usr/bin/python
# encoding=utf-8

import re
import jieba

fs = open("train-data.txt", "w")
fw = open("dict2.txt", "w")

dict = {}
tags = {}

def listRindex(alist, value):
    return len(alist) - alist[-1::-1].index(value) -1

def match(s, t):
  rows = len(s)
  cols = len(t)
  dist = [[0 for x in range(cols)] for x in range(rows)]
  print dist
 
  for col in range(0, cols):
    for row in range(0, rows):
      if s[row] == t[col]:
        dist[row][col] = 1

  # match in forward
  matched = [-1 for x in range(rows)]
  matched_col = 0
  for row in range(0, rows):
    target_list =  dist[row][matched_col:cols]
    if max(target_list) == 1:
      matched[row] = matched_col + target_list.index(1)
      matched_col = matched[row] + 1
    if matched_col == cols:
      matched_col = 0

  # match in backward
  print dist
  fm = [-1 for x in range(rows)]
  fm_col = cols
  for row in reversed(range(0, rows)):
    target_list = dist[row][0:fm_col]
    print target_list
    if max(target_list) == 1:
      fm[row] = listRindex(target_list, 1)
      fm_col = fm[row]
    if fm_col == 0:
      fm_col = cols
  print matched
  print fm
  if matched.count(-1) < fm.count(-1):
    return matched
  return fm


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
    return 'Word:%s, Tag:%s, Parent:%d, Relation:%s, Id:%d, Add:%d' % (self.word, self.tag, id(self.parent), self.r, self.id, id(self))


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
      if len(seg_list) == 0:
        continue
      for s in seg_list:
        mo = re.search('\{(.*)\}:\{(.*)\}', s)
        entities = mo.group(1).split(',')
        states = mo.group(2).split(',')
        et = []
        ept = None
        ekey = ''
        for e in entities:
          if e == 'null':
            continue
          emo = re.search('(.*)\[(.*)\]', e)
          addToDict(emo.group(1))
          addToTag(emo.group(2))
          token = Token(emo.group(1), emo.group(2))
          ekey = ekey + token.word
          et.append(token)
          if token.tag == '实体':
            ept = token
        dup_e = False
        if ekey in token_dict:
          et = token_dict[ekey]
          dup_e = True
        else:
          token_dict[ekey] = et
        if not dup_e:
          for t in et:
            if t != ept:
              t.parent = ept
              if t.tag == '前置位置':
                t.r = 'pre_pos'
              elif t.tag == '后置位置':
                t.r = 'post_pos'
        else:
          ept = None
          for t in et:
            if t.tag == '实体':
              ept = t

        st = []
        spt = None
        skey = ''
        for s in states:
          smo = re.search('(.*)\[(.*)\]', s)
          addToDict(smo.group(1))
          addToTag(smo.group(2))
          token = Token(smo.group(1), smo.group(2))
          skey = skey + token.word
          st.append(token)
          if token.tag == '异常' or token.tag == '疾病' or token.tag=='正常':
            spt = token
        dup_s = False
        if skey in token_dict:
          st = token_dict[skey]
          dup_s = True
        else:
          token_dict[skey] = st
        if not dup_s: 
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
        else:
          spt = None
          for t in st:
            if t.tag == '异常' or token.tag == '疾病' or token.tag=='正常':
              spt = t

        if ept:
          if not ept.parent:
            ept.parent = spt
            ept.r = 'illness'
          else:
            if spt:
              print 'DEBUDEBUDEBUG'
              for t in tokens:
                print t
              print '2DEBDEBDEB'
              for t in et:
                print t
              print '3DEBDEB'
              for t in st:
                print t
              print ept
              print spt
              if not spt.parent and ept.parent != spt:
                spt.parent = ept.parent
                spt.r = 'and'
        elif spt:
          # Loop back to first root, set as parent with relation and
          for tt in reversed(tokens):
            if not tt.parent and spt != tt:
              spt.parent = tt
              spt.r = 'and'
              break

        if not dup_e:
          tokens = tokens + et
        if not dup_s:
          tokens = tokens + st
      print sentence
      for t in tokens:
        jieba.add_word(t.word, 10000000)
      seg_s = jieba.cut(sentence, HMM=False)
      token_id = 0
      seg_ss = []
      for sss in seg_s:
        sss = sss.encode('utf-8')
        seg_ss.append(sss)
        print type(sss)
        print sss
      token_word = []
      for t in tokens:
        token_word.append(t.word)
        print type(t.word)
        print t.word
      
      match_matrix = match(seg_ss, token_word)
      for x in seg_ss:
        print x
      for x in tokens:
        print x
      print match_matrix
      # fill token_id for matched tokens
      for index in range(0, len(match_matrix)):
        if match_matrix[index] != -1:
           tokens[match_matrix[index]].id = index+2
      new_parts = []
      new_parts.append('1') # f0
      new_parts.append('root')      # f1
      new_parts.append('_')      # f2
      new_parts.append('None')      # f3
      new_parts.append('None')      # f4
      new_parts.append('_')      # f5
      new_parts.append('0')      # f6
      new_parts.append('_')      # f7
      new_parts.append('_')      # f8
      new_parts.append('SpaceAfter=No') # f9
      processed_list.append(new_parts)
      lastNone = 1
      for index in range(0, len(seg_ss)):
        token = None
        if match_matrix[index] != -1:
          token = tokens[match_matrix[index]]
        print type(seg_ss[index])
        print type(token)
        print seg_ss[index]
        print token
        new_parts = []
        new_parts.append(str(index+2)) # f0
        new_parts.append(seg_ss[index])      # f1
        new_parts.append('_')      # f2
        new_parts.append(token.tag if token else 'None')      # f3
        new_parts.append(token.tag if token else 'None')      # f4
        new_parts.append('_')      # f5
        new_parts.append(str(token.parent.id) if token and token.parent else ('1' if token else str(lastNone)))      # f6
        new_parts.append(token.r if token else '_')      # f7
        new_parts.append('_')      # f8
        new_parts.append('SpaceAfter=No') # f9
        processed_list.append(new_parts)
        if token == None:
          lastNone = index + 2
      
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

