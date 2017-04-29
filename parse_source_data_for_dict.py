#!/usr/bin/python

fs = open("sentence.txt", "w")
fw = open("dict.txt", "w")
dict = {}
with open("source_data.txt", "r") as fp:
  for line in fp:
   if line.startswith("sentence"):
     sen = line[10:-2]
     fs.write(sen)
     fs.write("\n")
   elif len(line) > 0:
     parts = line.split(',')
     for part in parts:
       pp = part.split('=')
       if len(pp) == 2:
         if pp[1] in dict:
           dict[pp[1]] += 1
         else:
           dict[pp[1]] = 1

fs.close()
for key in dict:
  fw.write(key)
  fw.write(' ')
  fw.write(str(dict[key]))
  fw.write('\n')
fw.close 

