#!/usr/bin/python

fs = open("dev-data0.txt", "w")
fw = open("dict4.txt", "w")

dict = {}
with open("dev-data.txt", "r") as fp:
  for line in fp:
    parts = line.split('\t')
    if len(parts) == 10:
      new_parts = []
      new_parts.append(parts[0]) # f0
      new_parts.append(parts[1]) # f1
      new_parts.append(parts[1]) # f2
      new_parts.append(parts[2]) # f3
      new_parts.append(parts[3]) # f4
      new_parts.append(parts[4]) # f5
      new_parts.append(parts[6]) # f6
      new_parts.append(parts[7]) # f7
      new_parts.append(parts[8]) # f8
      new_parts.append(parts[9]) # f9
      fs.write('\t'.join(new_parts))
    else:
      fs.write(line)

fs.close()
for key in dict:
  fw.write(key)
  fw.write(' ')
  fw.write(str(dict[key]))
  fw.write('\n')
fw.close 

