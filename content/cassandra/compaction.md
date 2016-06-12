title: Cassandra Compaction Strategy
date: 2016-05-02
description: A tutorial on Docker
tags: docker, kubernets, spark, programming, hadoop, bigdata, yarn

### Compaction Strategy
Cassandra flushes the memtables to disk as SSTables. There could be many SSTables. Cassandra merges several tables into one table by using the process called Compaction.

Two types of compaction

	:::text
	Minor and 
	Major

Minor compaction is triggered automatically whenever a new sstable is being created. May remove all tombstones
ompacts sstables of equal size in to one [initially memtable flush size] when minor compaction threshold is reached [4 by default]. 

Major Compaction is manually triggered using nodetool. Can be applied over a column family over a time
Compacts all the sstables of a CF in to 1
Compacts the SSTables and marks delete over unneeded SSTables. GC takes care of freeing up that space




