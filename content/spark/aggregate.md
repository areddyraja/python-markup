title: Big Data with Apache Spark
date: 2016-05-02
description: A tutorial on Apache Spark
tags: spark, programming, hadoop, bigdata, yarn

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


####Prnting the values from an iterator

	:::scala
	val data = 1 to 50
	val distData = sc.parallelize(data,10)
	distData.mapPartitionsWithIndex( (index: Int, it: Iterator[Int]) =>it.toList.map(x => if (index == 5 ) {Some(x)}).iterator).collect

	:::scala
	val z2 = sc.parallelize(List("1","12","23","345","4567"),2)
	z2.aggregate("")((x,y) => math.max(x.length, y.length).toString, (x,y) => x + y)
	res141: String = 42


	:::scala
	val z5 = sc.parallelize(List("1","12","23","345","4567"),2)
	z5.mapPartitionsWithIndex( (index: Int, it: Iterator[String]) =>it.toList.map(x =>  if (index == 0) {println(x)}).iterator).collect
	z5.aggregate("")((x,y) => math.min(x.length, y.length).toString, (x,y) => x + y)


	:::scala
	z4.aggregate("")((x,y) => math.min(x.length, y.length).toString, (x,y) => x + y)
	res141: String = 11 -- seems to be a problem


####Aggregate By Key
Ok, I admit, this one drives me a bit nuts.  Why wouldn’t we just use reduceByKey?  I don’t feel smart enough to know when to use aggregateByKey over reduceByKey.  For example, the same results may be produced:

Spark aggregateByKey example
 
	:::scala
val filteredRows = babyNames.filter(line => !line.contains("Count")).map(line => line.split(","))
filteredRows: org.apache.spark.rdd.RDD[Array[String]] = MappedRDD[546] at map at <console>:14
 
	:::scala
	filteredRows.map(n => (n(1),n(4).toInt)).reduceByKey((v1,v2) => v1 + v2).collect
	res452: Array[(String, Int)] = Array((BRADEN,39), (MATTEO,279), (HAZEL,133), (SKYE,63), (JOSUE,404), (RORY,12), (NAHLA,16), (ASIA,6), (MEGAN,581), (HINDY,254), (ELVIN,26), (AMARA,10), (CHARLOTTE,1737), (BELLA,672), (DANTE,246), (PAUL,712), (EPHRAIM,26), (ANGIE,295), (ANNABELLA,38), (DIAMOND,16), (ALFONSO,6), (MELISSA,560), (AYANNA,11), (ANIYAH,365), (DINAH,5), (MARLEY,32), (OLIVIA,6467), (MALLORY,15), (EZEQUIEL,13), (ELAINE,116), (ESMERALDA,71), (SKYLA,172), (EDEN,199), (MEGHAN,128), (AHRON,29), (KINLEY,5), (RUSSELL,5), (TROY,88), (MORDECHAI,521), (JALIYAH,10), (AUDREY,690), (VALERIE,584), (JAYSON,285), (SKYLER,26), (DASHIELL,24), (SHAINDEL,17), (AURORA,86), (ANGELY,5), (ANDERSON,369), (SHMUEL,315), (MARCO,370), (AUSTIN,1345), (MITCHELL,12), (SELINA,187), (FATIMA,421), (CESAR,292), (CAR...
 
 
	filteredRows.map ( n => (n(1), n(4))).aggregateByKey(0)((k,v) => v.toInt+k, (v,k) => k+v).sortBy(_._2).collect
 

