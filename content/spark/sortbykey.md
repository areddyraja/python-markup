title: Sort By Key
date: 2016-05-02
description: A tutorial on Apache Spark
tags: spark, programming, hadoop, bigdata, yarn

###Sort By Key
This simply sorts the (K,V) pair by K.

Spark sortByKey example
sortByKey([ascending], [numTasks])
 
	:::scala
	val filteredRows = babyNames.filter(line => !line.contains("Count")).map(line => line.split(","))
	filteredRows: org.apache.spark.rdd.RDD[Array[String]] = MappedRDD[546] at map at <console>:14
	 
	filteredRows.map ( n => (n(1), n(4))).sortByKey().foreach (println _)
	 
	filteredRows.map ( n => (n(1), n(4))).sortByKey(false).foreach (println _) // opposite order
	 
