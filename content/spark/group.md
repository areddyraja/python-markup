title: Group By
date: 2016-05-02
description: A tutorial on Apache Spark
tags: spark, programming, hadoop, bigdata, yarn

###groupBy

Spark RDD groupBy function returns an RDD of grouped items.
grupBy applies function to the source RDD and will create a new RDD as with the individual groups and the list of items in that group. 
The shuffling may happen across the partitions.

The new RDD will have a key, which is group and list of items in that group.
The method does not use the local combiner within the partition to reduce the data transfer

Similar to reduceByKey, groupBy has three variants

* groupBy(function) : generares output with existing partitioner
* groupBy(function, [numPartition]) : Number of partions given by numPartition
* groupBy(partitioner, function) : generate the object referenced by the partitioner function


####Example 1:
	:::scala
	val x = sc.parallelize(Array("Joseph", "Jimmy", "Tina",
     		"Thomas", "James", "Cory",
     		"Christine", "Jackeline", "Juan"), 3)
	x: org.apache.spark.rdd.RDD[String] = ParallelCollectionRDD[16] at parallelize at <console>:21

	val y = x.groupBy(word => word.charAt(0))
	y: org.apache.spark.rdd.RDD[(Char, Iterable[String])] = ShuffledRDD[18] at groupBy at <console>:23

	y.collect
	res0: Array[(Char, Iterable[String])] = Array((T,CompactBuffer(Tina, Thomas)), (C,CompactBuffer(Cory,
	 	Christine)), (J,CompactBuffer(Joseph, Jimmy, James, Jackeline, Juan)))

Shorter syntax

	:::scala
	val y = x.groupBy(_.charAt(0))
	y: org.apache.spark.rdd.RDD[(Char, Iterable[String])] = ShuffledRDD[3] at groupBy at <console>:23

	y.collect
	res1: Array[(Char, Iterable[String])] = Array((T,CompactBuffer(Tina, Thomas)), (C,CompactBuffer(Cory,
	 	Christine)), (J,CompactBuffer(Joseph, Jimmy, James, Jackeline, Juan)))


####Example 2

	:::scala
	case class Item(id:String, name:String, unit:Int, companyId:String)
	case class Company(companyId:String, name:String, city:String)
	val i1 = Item("1", "first", 2, "c1")
	val i2 = i1.copy(id="2", name="second")
	val i3 = i1.copy(id="3", name="third", companyId="c2")
	val items = sc.parallelize(List(i1,i2,i3))
	org.apache.spark.rdd.RDD[Item] = ParallelCollectionRDD[14] at parallelize at <console>:20


	val c1 = Company("c1", "company-1", "city-1")
	val c2 = Company("c2", "company-2", "city-2")
	val companies = sc.parallelize(List(c1,c2))
	val groupedItems = items.groupBy( x => x.companyId) 
	groupedItems: org.apache.spark.rdd.RDD[(String, Iterable[Item])] = ShuffledRDD[16] at groupBy at <console>:22
	val groupedComp = companies.groupBy(x => x.companyId)
	groupedComp: org.apache.spark.rdd.RDD[(String, Iterable[Company])] = ShuffledRDD[18] at groupBy at <console>:20
	groupedItems.join(groupedComp).take(10).foreach(println)

	14/12/12 00:52:32 INFO DAGScheduler: Job 5 finished: take at <console>:35, took 0.021870 s
	(c1,(CompactBuffer(Item(1,first,2,c1), Item(2,second,2,c1)),CompactBuffer(Company(c1,company-1,city-1))))
	(c2,(CompactBuffer(Item(3,third,2,c2)),CompactBuffer(Company(c2,company-2,city-2))))

###Multi Columns Map/Reduce with Apache Spark

	:::scala
	val sales=sc.parallelize(List(
	   ("West",  "Apple",  2.0, 10),
	   ("West",  "Apple",  3.0, 15),
	   ("West",  "Orange", 5.0, 15),
	   ("South", "Orange", 3.0, 9),
	   ("South", "Orange", 6.0, 18),
	   ("East",  "Milk",   5.0, 5)))


	sales.map{ case (store, prod, amt, units) => ((store, prod), (amt, amt, amt, units)) }.
	  reduceByKey((x, y) => 
	   (x._1 + y._1, math.min(x._2, y._2), math.max(x._3, y._3), x._4 + y._4)).collect

###Aggregate

	:::scala
	val z = sc.parallelize(List(1,2,3,4,5,6), 2)
	z.aggregate(0)(_+_,_+_)

Aggregate definition

	:::scala
	def aggregate[U](zeroValue: U)(seqOp: (U, T) => U, combOp: (U, U) => U)(implicit scala.reflect.ClassTag[U]): U 

Fist operation *seqOp* is applied on each partition and second opertion *combOp* is applied on the result aggregates

	:::scala
	def myfunc(index: Int, iter:Iterator[Int]) : Iterator[String] = {
		iter.toList.map(x=>"[partid:" + index +  ",val:" +  x + "]").iterator
	}

	z.mapPartitionsWithIndex(myfunc).collect

	res2: Array[String] = Array([partid:0,val:1], [partid:0,val:2], [partid:0,val:3], [partid:1,val:4], [partid:1,val:5], [partid:1,val:6])

	z.aggregate(0)(math.max(_,_),_+_)
	z.mapPartitionsWithIndex( (index: Int, it: Iterator[Int]) =>it.toList.map(x =>  if(index == 1) {x}).iterator).collect

###MapPartitionWithIndex

	:::scala
	val data = 1 to 50
	val distData = sc.parallelize(data,10)
	distData.mapPartitionsWithIndex( (index: Int, it: Iterator[Int]) =>it.toList.map(x => if (index == 5 ) {Some(x)}).iterator).collect

	val z2 = sc.parallelize(List("1","12","23","345","4567"),2)
	z2.aggregate("")((x,y) => math.max(x.length, y.length).toString, (x,y) => x + y)
	res141: String = 42

	val z5 = sc.parallelize(List("1","12","23","345","4567"),2)
	z5.mapPartitionsWithIndex( (index: Int, it: Iterator[String]) \
            =>it.toList.map(x =>  if (index == 0) {println(x)}).iterator).collect

	z5.aggregate("")((x,y) => math.min(x.length, y.length).toString, (x,y) => x + y)

	z4.aggregate("")((x,y) => math.min(x.length, y.length).toString, (x,y) => x + y)
	res141: String = 11 -- seems to be a problem

