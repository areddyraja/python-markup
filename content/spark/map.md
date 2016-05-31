title: Map
date: 2016-05-02
description: A tutorial on Apache Spark
tags: spark, programming, hadoop, bigdata, yarn


###Map
Map applies transformation function on each of the items in the RDD. The return value is also an RDD
####example 1

	:::jinja
	val fruits = sc.parallelize(List("orange", "apple", "kiwi", "kiwi", "rabbit", "avakado","mango", "grapes", "banana"), 3)
	val lengths = fruits.map(_.length)
	val fruit_lengths = fruits.zip(lengths)
	fruit_lengths.collect

####example 2

	:::scala
	val names = sc.parallelize(List("Peter","Paul","Mary","John","Harry", 2)
	names.map(_.toUppercase)
	val fruit_lengths = fruits.zip(lengths)
	fruit_lengths.collect

####MapValues (Pair)

The mapValues Takes the values of a RDD that consists of two-component tuples, and applies the provided function to transform each value. 
Then, it forms new two-component tuples using the key and the transformed value and stores them in a new RDD.

	:::scala
	def mapValues[U](f: V => U): RDD[(K, U)]

Example

	:::scala
	val a = sc.parallelize(List("dog", "tiger", "lion", "cat", "panther", "eagle"), 2)
	val b = a.map(x => (x.length, x))
	b.mapValues("x" + _ + "x").collect

	res5: Array[(Int, String)] = Array((3,xdogx), (5,xtigerx), (4,xlionx), (3,xcatx), 
		(7,xpantherx), (5,xeaglex))


###flatMap example

Spark RDD flatMap function returns a new RDD by first applying a function to all elements of this RDD, and then flattening the results.

One step more than RDD map operation, it accepts the argument function which returns array, list or sequence of elements instead of a single element.

As a final result it flattens all the elements of the resulting RDD in case individual elements are in form of list, array, sequence or any such collection.

Example

	:::scala
	val x = sc.parallelize(List("spark rdd example",  "sample example"), 2)

	val y = x.map(x => x.split(" ")) // split(" ") returns an array of words
	y.collect
	res0: Array[Array[String]] = Array(Array(spark, rdd, example), Array(sample, example))

	val y = x.flatMap(x => x.split(" "))
	y.collect
	res1: Array[String] = Array(spark, rdd, example, sample, example)

	val y = x.flatMap(_.split(" "))
	y.collect
	res2: Array[String] = Array(spark, rdd, example, sample, example)


####Map with Paritions
mapPartitions is a tool for performance optimization. It’s the same as “map”, but works with Spark RDD partitions.

#####Spark mapPartitions


	:::scala
	API: mapPartitions[U](f: (Iterator[T]) ⇒ Iterator[U], preservesPartitioning: Boolean = false)(implicit arg0:ClassTag[U]): RDD[U]

	val parallel = sc.parallelize(1 to 9, 3)
	parallel: org.apache.spark.rdd.RDD[Int] = ParallelCollectionRDD[450] at parallelize at <console>:12
	 
	parallel.mapPartitions( x => List(x.next).iterator).collect
	res383: Array[Int] = Array(1, 4, 7)
	 
	// compare to the same, but with default parallelize
	val parallel = sc.parallelize(1 to 9)
	parallel: org.apache.spark.rdd.RDD[Int] = ParallelCollectionRDD[452] at parallelize at <console>:12
	 
	parallel.mapPartitions( x => List(x.next).iterator).collect
	res384: Array[Int] = Array(1, 2, 3, 4, 5, 6, 7, 8)
	 

####Map with Partions Index

#####Spark mapPartitionsWithIndex examples

Similar to mapPartitions, but also provides a function with an Int value to indicate the index position of the partition.
	:::scala
	mapPartitionsWithIndex(func)

Return a new RDD by applying a function to each partition of this RDD, while tracking the index of the original partition. Indicates whether the input function preserves the partitioner, which should be unless this is a pair RDD and the input function doesn’t modify the keys.

	:::scala
	mapPartitionsWithIndex[U](f: (Int, Iterator[T]) ⇒ Iterator[U], preservesPartitioning: Boolean = false): RDD[U]
 
	:::scala
	val parallel = sc.parallelize(1 to 9)
	parallel: org.apache.spark.rdd.RDD[Int] = ParallelCollectionRDD[455] at parallelize at <console>:12
	 
	parallel.mapPartitionsWithIndex( (index: Int, it: Iterator[Int]) => it.toList.map(x => index + ", "+x).iterator).collect
	res389: Array[String] = Array(0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 7, 9)
	 
For example, if we change the above example to use a parallelize’d list with 3 slices, our output changes significantly:

Spark mapPartitionsWithIndex example with sliced collection
 
	:::scala
	val parallel = sc.parallelize(1 to 9, 3)
	parallel: org.apache.spark.rdd.RDD[Int] = ParallelCollectionRDD[457] at parallelize at <console>:12
	 
	parallel.mapPartitionsWithIndex( (index: Int, it: Iterator[Int]) => it.toList.map(x => index + ", "+x).iterator).collect
	res390: Array[String] = Array(0, 1, 0, 2, 0, 3, 1, 4, 1, 5, 1, 6, 2, 7, 2, 8, 2, 9)
	 


