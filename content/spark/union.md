title: Union
date: 2016-05-02
description: A tutorial on Apache Spark
tags: spark, programming, hadoop, bigdata, yarn

###Union

union(a different rdd)
Simple.  Return the union of two RDDs

Spark union transformation example

	:::scala
	val parallel = sc.parallelize(1 to 9)
	parallel: org.apache.spark.rdd.RDD[Int] = ParallelCollectionRDD[477] at parallelize at <console>:12
	 
	val par2 = sc.parallelize(5 to 15)
	par2: org.apache.spark.rdd.RDD[Int] = ParallelCollectionRDD[478] at parallelize at <console>:12
	 
	parallel.union(par2).collect
	res408: Array[Int] = Array(1, 2, 3, 4, 5, 6, 7, 8, 9, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15)
	 


