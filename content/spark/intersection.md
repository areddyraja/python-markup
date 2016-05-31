title: Intersection
date: 2016-05-02
description: A tutorial on Apache Spark
tags: spark, programming, hadoop, bigdata, yarn

###Intersection

Simple.  Similar to union but return the intersection of two RDDs

	:::scala
	intersection(other: RDD[T]): RDD[T]


Spark intersection transformation example

	:::scala
	val parallel = sc.parallelize(1 to 9)
	parallel: org.apache.spark.rdd.RDD[Int] = ParallelCollectionRDD[477] at parallelize at <console>:12
	 
	val par2 = sc.parallelize(5 to 15)
	par2: org.apache.spark.rdd.RDD[Int] = ParallelCollectionRDD[478] at parallelize at <console>:12
	 
	parallel.intersection(par2).collect
	res409: Array[Int] = Array(8, 9, 5, 6, 7)
	 




