#!/usr/bin/python

fs = open("train-data.txt", "w")
fw = open("dict1.txt", "w")

dict = {}
tags = {}
with open("data-demo.txt", "r") as fp:
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
      for s in seg_list:
        parts = s.split('\t')
        assert len(parts) > 4
        seged_list.append(parts)
        test_sen = test_sen + parts[1]
        new_parts = []
        new_parts.append(parts[0]) # f0
        new_parts.append(parts[1]) # f1
        new_parts.append(parts[1]) # f2
        new_parts.append(parts[2]) # f3
        new_parts.append(parts[2]) # f4
        new_parts.append('_')      # f5
        new_parts.append('_')      # f6
        new_parts.append(parts[3]) # f7
        new_parts.append('_')      # f8
        new_parts.append('SpaceAfter=No') # f9
        processed_list.append(new_parts)
        if parts[1] in dict:
          dict[parts[1]] += 1
        else:
          dict[parts[1]] = 1
        if parts[2] in tags:
          tags[parts[2]] += 1
        else:
          tags[parts[2]] = 1
      assert sentence == test_sen
      fs.write('# sent_id = %d\n' % sent_num)
      sent_num += 1
      fs.write('# text = ')
      fs.write(test_sen)
      fs.write('\n')
      for np in processed_list:
        fs.write('\t'.join(np))
        fs.write('\n')
      fs.write('\n')
      sentence = ''
      seg_list = []

    elif line.startswith("sentence"):
      sentence = line[10:-4]
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

