title: MapReduce with python
date: 2016-05-02
description: MapReduce with python
tags: python, pymr, programming, hadoop, bigdata, yarn

#Lab2 : Map Reduce Python

Mapper code

```

import re
import sys

for line in sys.stdin:
  val = line.strip()
  (year, temp, q) = (val[15:19], val[87:92], val[92:93])
  if (temp != "+9999" and re.match("[01459]", q)):
        print "%s\t%s" % (year, temp)
Reducer

import sys

(last_key, max_val) = (None, -sys.maxint)
for line in sys.stdin:
  (key, val) = line.strip().split("\t")
  if last_key and last_key != key:
        print "%s\t%s" % (last_key, max_val)
        (last_key, max_val) = (key, int(val))
  else:
        (last_key, max_val) = (key, max(max_val, int(val)))

if last_key:
  print "%s\t%s" % (last_key, max_val)

```

##Execute Map Reduce

cat input/ncdc/sample.txt |
ch02/src/main/python/max_temperature_map.py | sort | ch02/src/main/python/max_temperature_reduce.py

Output

1949        111
    1950    22

