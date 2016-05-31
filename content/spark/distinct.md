title: Distinct
date: 2016-05-02
description: A tutorial on Apache Spark
tags: spark, programming, hadoop, bigdata, yarn

###Distinct

Return a new RDD with distinct elements within a source RDD

	:::scala
	distinct(): RDD[T]

Spark distinct transformation example
 
	:::scala
	val parallel = sc.parallelize(1 to 9)
	parallel: org.apache.spark.rdd.RDD[Int] = ParallelCollectionRDD[477] at parallelize at <console>:12
	 
	val par2 = sc.parallelize(5 to 15)
	par2: org.apache.spark.rdd.RDD[Int] = ParallelCollectionRDD[478] at parallelize at <console>:12
	 
	parallel.union(par2).distinct.collect
	res412: Array[Int] = Array(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15)
 

