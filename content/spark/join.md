title: Join
date: 2016-05-02
description: A tutorial on Apache Spark
tags: spark, programming, hadoop, bigdata, yarn

##Join

It’s joining of two datasets.  
Other joins are available as well such as leftOuterJoin and rightOuterJoin.

Spark join example, leftOuterJoin example, rightOuterJoin example
 
	:::scala
	val names1 = sc.parallelize(List("abe", "abby", "apple")).map(a => (a, 1))
	names1: org.apache.spark.rdd.RDD[(String, Int)] = MappedRDD[1441] at map at <console>:14
	 
	val names2 = sc.parallelize(List("apple", "beatty", "beatrice")).map(a => (a, 1))
	names2: org.apache.spark.rdd.RDD[(String, Int)] = MappedRDD[1443] at map at <console>:14
	 
	names1.join(names2).collect
	res735: Array[(String, (Int, Int))] = Array((apple,(1,1)))
	 
	names1.leftOuterJoin(names2).collect
	res736: Array[(String, (Int, Option[Int]))] = Array((abby,(1,None)), (apple,(1,Some(1))), (abe,(1,None)))
	 
	names1.rightOuterJoin(names2).collect
	res737: Array[(String, (Option[Int], Int))] = Array((apple,(Some(1),1)), (beatty,(None,1)), (beatrice,(None,1)))

###Joining two CSV files with common join key 

	:::scala
	val format = new java.text.SimpleDateFormat("yyyy-MM-dd")

	case class Register (d: java.util.Date, uuid: String, cust_id: String, lat: Float, lng: Float)
	case class Click (d: java.util.Date, uuid: String, landing_page: Int)

	val reg = sc.textFile("reg.tsv").map(_.split("\t")).map(
	 r => (r(1), Register(format.parse(r(0)), r(1), r(2), r(3).toFloat, r(4).toFloat))
	)

	reg.take(2)
	res19: Array[(String, Register)] = Array((15dfb8e6cc4111e3a5bb600308919594,Register \
             (Fri Mar 02 00:00:00 IST 14,15dfb8e6cc4111e3a5bb600308919594,1,33.659943,-117.95812)), \
             (81da510acc4111e387f3600308919594,Register(Tue Mar 04 00:00:00 IST 2014, \
              81da510acc4111e387f3600308919594,2,33.85701,-117.85574)))

	val clk = sc.textFile("clk.tsv").map(_.split("\t")).map(
	  c => (c(1), Click(format.parse(c(0)), c(1), c(2).trim.toInt))
	)
	clk.take(2)
	res18: Array[(String, Click)] = Array((15dfb8e6cc4111e3a5bb600308919594,Click(Tue Mar 04 00:00:00 IST 2014,15dfb8e6cc4111e3a5bb600308919594,11)), (81da510acc4111e387f3600308919594,Click(Thu Mar 06 00:00:00 IST 2014,81da510acc4111e387f3600308919594,61)))


	reg.join(clk).take(2)
	res17: Array[(String, (Register, Click))] = Array((81da510acc4111e387f3600308919594,(Register(Tue Mar 04 00:00:00 IST 2014,81da510acc4111e387f3600308919594,2,33.85701,-117.85574),Click(Thu Mar 06 00:00:00 IST 2014,81da510acc4111e387f3600308919594,61))), (15dfb8e6cc4111e3a5bb600308919594,(Register(Fri Mar 02 00:00:00 IST 14,15dfb8e6cc4111e3a5bb600308919594,1,33.659943,-117.95812),Click(Tue Mar 04 00:00:00 IST 2014,15dfb8e6cc4111e3a5bb600308919594,11))))


###Joining and filtering data from two data sets 

####method 1

	:::scala
	val f = sc.textFile("README.md")
	val wc = f.flatMap(l => l.split(" ")).
	map(word => (word, 1)).
	reduceByKey(_ + _)
	wc.filter(_._1 == "Spark").collect()
	res0: Array[(String, Int)] = Array((Spark,18))

	val f2 = sc.textFile("docs/contributing-to-spark.md")
	val wc2 = f2.flatMap(l => l.split(" ")).
	map(word => (word, 1)).
	reduceByKey(_ + _)
	wc.join(wc2).map(x => (x._1,x._2._1 + x._2._2)).
	filter(_._1 == "Spark").
	collect()
	res3: Array[(String, Int)] = Array((Spark,20))

####method 2

	:::scala
	val wc1 = sc.textFile("README.md").
	flatMap(line => line.split(" ")).
	map(word => (word, 1))
	val wc2 = sc.textFile("docs/contributing-to-spark.md").
	flatMap(line => line.split(" ")).
	map(word => (word, 1))
	wc1.union(wc2).
	reduceByKey(_ + _).
	filter(_._1 == "Spark").

####method3

	:::scala
	sc.textFile("README.md").
	union(sc.textFile("docs/contributing-to-spark.md")).
	flatMap(_.split(" ")).
	filter(_ == "Spark").
	count()
	res2: Long = 20

###Writing into a File
             
	:::scala
	import java.io.File
	import java.io.PrintWriter
	 
	import scala.io.Source
	 
	object Write {
	  def main(args: Array[String]) {
	    val writer = new PrintWriter(new File("Write.txt"))
	 
	    writer.write("Hello Developer, Welcome to Scala Programming.")
	    writer.close()
	 
	    Source.fromFile("Write.txt").foreach { x => print(x) }
	  }
	 
	}


###Map Side Join
To join a large table with small tables, and to avoid sending large data across partitions, map side is used.
It is also called replicated join or broadcast join.

Generally fact tables are large and dimension tables are small.

To build a single Fact Table from multiple tab

	:::data

	// Fact table
	val flights = sc.parallelize(List(
	  ("SEA", "JFK", "DL", "418",  "7:00"),
	  ("SFO", "LAX", "AA", "1250", "7:05"),
	  ("SFO", "JFK", "VX", "12",   "7:05"),
	  ("JFK", "LAX", "DL", "424",  "7:10"),
	  ("LAX", "SEA", "DL", "5737", "7:10")))  
	   
	// Dimension table
	val airports = sc.parallelize(List(
	  ("JFK", "John F. Kennedy International Airport", "New York", "NY"),
	  ("LAX", "Los Angeles International Airport", "Los Angeles", "CA"),
	  ("SEA", "Seattle-Tacoma International Airport", "Seattle", "WA"),
	  ("SFO", "San Francisco International Airport", "San Francisco", "CA")))
	   
	// Dimension table
	val airlines = sc.parallelize(List(
	  ("AA", "American Airlines"), 
	  ("DL", "Delta Airlines"), 
	  ("VX", "Virgin America")))   


The following should be the result

	:::Result
	Seattle           New York       Delta Airlines       418   7:00
	San Francisco     Los Angeles    American Airlines    1250  7:05
	San Francisco     New York       Virgin America       12    7:05
	New York          Los Angeles    Delta Airlines       424   7:10
	Los Angeles       Seattle        Delta Airlines       5737  7:10


The program is given below:

	:::spark
	val airportsMap = sc.broadcast(airports.map{case(a, b, c, d) => (a, c)}.collectAsMap)
	val airlinesMap = sc.broadcast(airlines.collectAsMap)
	flights.map{case(a, b, c, d, e) => 
	   (airportsMap.value.get(a).get, 
	    airportsMap.value.get(b).get, 
	    airlinesMap.value.get(c).get, d, e)}.collect

#####How it works
RDD is creates for each of the tables.
Airports and Airlines are dimension tables that we are going to use in map-side join.
Each of this table is converted to Map and broadcast to each execution node.

Assuming the flights table is large, the map fucntion would get executed in each of the partition for each row.
The map side join helps not to shuffle the large table and get a good performance.

###Left outerjoin
The program outlines the join of two data sets using scala program.



