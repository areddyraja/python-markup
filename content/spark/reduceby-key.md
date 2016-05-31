title: ReduceByKey
date: 2016-05-02
description: A tutorial on Apache Spark
tags: spark, programming, hadoop, bigdata, yarn

ReduceBy Key has three variants

* reduceByKey(function)   : generates hash-partitioned output for the existing partitioner
* reduceByKey(function, [numPartition]): number of partitions given by numPartition
* reduceByKey(partitioner, function): uses partitioner specified

reduceByKey shuffles data from multiple partitions as creates another RDD.
It merges the data locally using the same function before sending data across partitions.
Should only be used with Key and values.
Accepts the commutative and Associative function as an argument.

###Example

	:::scala
	val x = sc.parallelize(Array(("a", 1), ("b", 1), ("a", 1),
	      ("a", 1), ("b", 1), ("b", 1),
	      ("b", 1), ("b", 1)), 3)
	x: org.apache.spark.rdd.RDD[(String, Int)] = ParallelCollectionRDD[1] at parallelize at <console>:21

Applying reduceByKey operation on x

	:::scala
	val y = x.reduceByKey((accum, n) => (accum + n))
	y: org.apache.spark.rdd.RDD[(String, Int)] = ShuffledRDD[2] at reduceByKey at <console>:23

	y.collect
	res0: Array[(String, Int)] = Array((a,3), (b,5))

Another way of reducing the function:

	:::scala
	val y = x.reduceByKey(_ + _)
	y: org.apache.spark.rdd.RDD[(String, Int)] = ShuffledRDD[3] at reduceByKey at <console>:23

	y.collect
	res1: Array[(String, Int)] = Array((a,3), (b,5))

Defnining associative function separately

	:::scala
	def sumFunc(accum:Int, n:Int) =  accum + n
	sumFunc: (accum: Int, n: Int)Int

	val y = x.reduceByKey(sumFunc)
	y: org.apache.spark.rdd.RDD[(String, Int)] = ShuffledRDD[4] at reduceByKey at <console>:25

	y.collect
	res2: Array[(String, Int)] = Array((a,3), (b,5))

###ReduceByKey 
This function provides the well-known reduce functionality in Spark. 

	:::scala
	def reduceByKey(func: (V, V) => V): RDD[(K, V)]

The function func you provide, should be commutative in order to generate reproducible results.

	:::scala
	val a = sc.parallelize(List("dog", "cat", "owl", "gnu", "ant"), 2)
	val b = a.map(x => (x.length, x))
	b.reduceByKey(_ + _).collect
	res86: Array[(Int, String)] = Array((3,dogcatowlgnuant))

	val a = sc.parallelize(List("dog", "tiger", "lion", "cat", "panther", "eagle"), 2)
	val b = a.map(x => (x.length, x))
	b.reduceByKey(_ + _).collect
	res87: Array[(Int, String)] = Array((4,lion), (3,dogcat), (7,panther), (5,tigereagle))

####Reduce By key - Using tuples

	:::scala
	val views=sc.parallelize(List(
	   ("US",  "Nov", "News",  100, 300),
	   ("US",  "Dec", "BreakingBad",  200, 2000),
	   ("US",  "Jan", "BreakingBad", 300, 3002),
	   ("US",  "Mar", "Friends", 122, 1230),
	   ("US",  "Apr", "Friends", 10,100),
	   ("US",  "May", "Friends", 20, 200),
	   ("US",  "Jun", "The Robot", 122,150),
	   ("US",  "Jul", "The Robot", 12, 1043),
	   ("India",  "Dec", "The Robot",  200, 2048),
	   ("India",  "Jan", "BreakingBad", 300, 900),
	   ("India",  "Mar", "BreakingBad", 122, 366),
	   ("India",  "Apr", "Friends", 10, 30),
	   ("India",  "May", "The Robot", 20, 80),
	   ("India",  "Jun", "Friends", 122, 488),
	   ("India",  "Jul", "BruceLee", 122, 488)))

Let us split the data into two tuples. First one will have the (country, program) and second one will have (likes, watched mins as the tuple).

	:::scala
	val views_counts = views.map{case (country, month, program, likes, mins) => ((country,program),(likes, mins) )}.reduceByKey((x,y)=>((x._1+y._1),(x._2+y._2))).collect

output

	:::scala
	views_counts: Array[((String, String), (Int, Int))] = Array(((India,The Robot),(220,2128)), ((US,BreakingBad),(500,5002)), ((US,News),(100,300)), ((India,Friends),(132,518)), ((India,BruceLee),(122,488)), ((US,Friends),(152,1530)), ((India,BreakingBad),(422,1266)), ((US,The Robot),(134,1193))

#####How it works
The first step is to defnine a map that returns tuples.
A key-value tuple is defined where key is also a tuple containing country and program. The value is also a tuple with likes and views.

	:::scala
	views.map{case (country, month, program, likes, mins) => ((country,program),(likes, mins) )}

The next step is to reduce values by key.
The reduce function reduces the two values. x being the previus values and y being the current values. x and y are tuples, each containing (country,program),(likes, mins).
Reduce is an associative operation and it works by adding two values first, and then take next set of values and keep adding till all the records are finished.
The second tuple has (likes, mins). The numbers for the same key are added to reduce to a single record.
The reduce step reduces all the common keys(country,program combination) into a single record.

	:::scala
	reduceByKey((x,y)=>((x._1+y._1),(x._2+y._2))

####Multi Columns Map/Reduce with Apache Spark

The following code groups the data by store and product.
The data has store, product, amout, units as the columns.


	:::scala
	val sales=sc.parallelize(List(
	   ("West",  "Apple",  2.0, 10),
	   ("West",  "Apple",  3.0, 15),
	   ("West",  "Orange", 5.0, 15),
	   ("South", "Orange", 3.0, 9),
	   ("South", "Orange", 6.0, 18),
	   ("East",  "Milk",   5.0, 5)))

The single line spark/scala would be

	:::scala
	sales.map{ case (store, prod, amt, units) => ((store, prod), (amt, amt, amt, units)) }.
	   reduceByKey((x, y) =>  
	   (x._1 + y._1, math.min(x._2, y._2), math.max(x._3, y._3), x._4 + y._4)).collect

The results is shown below:

	:::scala
	res: Array[((String, String), (Double, Double, Double, Int))] = Array(
	  ((West, Orange), (5.0, 5.0, 5.0, 15)), 
	  ((West, Apple),  (5.0, 2.0, 3.0, 25)), 
	  ((East, Milk),   (5.0, 5.0, 5.0, 5)), 
	  ((South, Orange),(9.0, 3.0, 6.0, 27)))

#####How it works
The first step to define key and value. The key is the combination of (store, prod) and the value is mapped to
(amt, amt, amt, units), which arenothing but, min, max, sum and total units.
This step is defined in 

	:::scala
	sales.map{ case (store, prod, amt, units) => ((store, prod), (sum, amt, amt, units)) }.

The next step to reduce the values by key (*reduceByKey((x, y) => **
The function x is the reduction of previous values and y is the current value. Both x and y are tuples containing
(sum, min, max,units)

Now the meaning of 

reduceByKey((x, y) => 
  (x._1 + y._1, math.min(x._2, y._2), math.max(x._3, y._3), x._4 + y._4)).collect

Sum of previous and current values is given by  **x._1 + y._1**
Minimum of previous and current is given by **math.min(x._2, y._2)**
Maximum of previos and current is given by **math.max(x._3, y._3)**
Sum of previos and current units is given by **x._4 + y._4**


