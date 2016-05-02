title: Big Data with Hadoop
date: 2016-05-02
description: MapReduce with MRJob
tags: python, streaming, mrjob, MRJob, programming, hadoop, bigdata, yarn


#Lab2 : Map Reduce with MRJob

In this lab you will learn how to use MRJob, a streaming python library to write and run Map Reduce Programs.

###Word Count

Example of Word Count as a MRJob

Source Code

```python

from mrjob.job import MRJob

class MRWordCountUtility(MRJob):

        def __init__(self, *args, **kwargs):
            super(MRWordCountUtility, self).__init__(*args, **kwargs)
            self.chars = 0
            self.words = 0
            self.lines = 0

        def mapper(self, _, line):
            # Don't actually yield anything for each line. Instead, collect them
            # and yield the sums when all lines have been processed. The results
            # will be collected by the reducer.
            self.chars += len(line) + 1  # +1 for newline
            self.words += sum(1 for word in line.split() if word.strip())
            self.lines += 1

        def mapper_final(self):
            yield('chars', self.chars)
            yield('words', self.words)
            yield('lines', self.lines)

        def reducer(self, key, values):
            yield(key, sum(values))


if __name__ == '__main__':
        MRWordCountUtility.run()
```

Run Locally

python mr_wc.py ../../README.rst
Run on Hadoop

python mr_wc.py -r hadoop  hdfs://localhost:9000/hadoop-book/wikipedia.txt
Max Temperature

Find Maximum Temperature from ncdc data used in Lab2 Map Reduce for Java Earlier.

Input Data

0067011990999991950051507004+68750+023550FM-12+038299999V0203301N00671220001CN9999999N9+00001+99999999999
0043011990999991950051512004+68750+023550FM-12+038299999V0203201N00671220001CN9999999N9+00221+99999999999
0043011990999991950051518004+68750+023550FM-12+038299999V0203201N00261220001CN9999999N9-00111+99999999999
0043012650999991949032412004+62300+010750FM-12+048599999V0202701N00461220001CN0500001N9+01111+99999999999
0043012650999991949032418004+62300+010750FM-12+048599999V0202701N00461220001CN0500001N9+00781+99999999999
Max Temperature

from mrjob.job import MRJob

class MRMaxTemperature(MRJob):

        def mapper(self, _, line):
            year = line[15:19]
            c_at_87 = line[87]
            if c_at_87 == '+':
                temp = line[88:92]
            else:
                temp = line[87:92]
            yield(year, temp)

        def reducer(self, year, temp):
            max_temp = max(temp)
            yield (year, max_temp)


if __name__ == '__main__':
        MRMaxTemperature.run()
Max Temperature with Combiner

from mrjob.job import MRJob

class MRMaxTemperatureCombiner(MRJob):

        def mapper(self, _, line):
            year = line[15:19]
            c_at_87 = line[87]
            if c_at_87 == '+':
                temp = line[88:92]
            else:
                temp = line[87:92]
            yield(year, temp)

        def combiner(self, year, temp):
            max_temp = max(temp)
            yield (year, max_temp)

        def reducer(self, year, temp):
            max_temp = max(temp)
            yield (year, max_temp)


if __name__ == '__main__':
        MRMaxTemperatureCombiner.run()
Execute Map Reduce

Assuming your code is in the directory :~/work/mrjob/mrjob/mrjob/examples. Execute the following command from that directory.

$ ./mr_max_temperature.py /home/ubuntu/work/hadoop-book/input/ncdc/sample.txt
Output

  /usr/bin/python2.7 /home/ubuntu/work/mrjob/mrjob/mrjob/
examples/mr_max_temperature_combiner.py
/home/ubuntu/work/hadoop-book/input/ncdc/sample.txt
       no configs found; falling back on auto-configuration
       no configs found; falling back on auto-configuration
       creating tmp directory /tmp/mr_max_temperature_combiner.
 ubuntu.20150319.055609.108006
       writing to /tmp/mr_max_temperature_combiner.ubuntu.20150319.055609.108006/step-0-mapper_part-00000
       Counters from step 1:
         (no counters found)
       writing to /tmp/mr_max_temperature_combiner.ubuntu.20150319.055609.108006/step-0-mapper-sorted
       > sort /tmp/mr_max_temperature_combiner.ubuntu.20150319.055609.108006/step-0-mapper_part-00000
       writing to /tmp/mr_max_temperature_combiner.ubuntu.20150319.055609.108006/step-0-reducer_part-00000
       Counters from step 1:
         (no counters found)
       Moving /tmp/mr_max_temperature_combiner.
  ubuntu.20150319.055609.108006/step-0-reducer_part-00000 ->
   /tmp/mr_max_temperature_combiner.ubuntu.20150319.055609.108006/output/part-00000
       Streaming final output from /tmp/mr_max_temperature_combiner.ubuntu.20150319.055609.108006/output
       removing tmp directory /tmp/mr_max_temperature_combiner.ubuntu.20150319.055609.108006
       "1949"  "0111"
       "1950"  "0022"

