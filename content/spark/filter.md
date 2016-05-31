title: Filter
date: 2016-05-02
description: A tutorial on Apache Spark
tags: spark, programming, hadoop, bigdata, yarn

###Filter
Filter method filters all the elements of the source RDD for which predicate is not satisfied and creates a new RDD.
Filter does not shuffle data across partitions.

Example

	:::scala
 	val x = sc.parallelize(1 to 10, 2)

	val y = x.filter(e => e%2==0) 
	y.collect
	res0: Array[Int] = Array(2, 4, 6, 8, 10)


A shorter syntax

	:::scala
	val y = x.filter(_ % 2 == 0)
	y.collect
	res1: Array[Int] = Array(2, 4, 6, 8, 10)


