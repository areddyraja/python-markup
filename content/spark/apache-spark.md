title: Big Data with Apache Spark
date: 2016-05-02
description: A tutorial on Apache Spark
tags: spark, programming, hadoop, bigdata, yarn

###Introduction
Apache Spark is the opensource distributed computing framework, more focussed on iterative computing. It relies on the computation graph for reliability and uses in-memory computing. It is a general purpose cluster computing Platform. Spark is built and developed at Berkeley labs. It is moved to Apache and is written in scala and has the APIs in scala, python and Java. 

Python spark is getting more popular than Spark Scala.

Apache Spark is multiple times faster than its predecessor Hadoop due to its design to use memory.
Hadoop primarily provides MapReduce paradigm, where Apache Spark offers MapReduce and a rich set of API for computing.

Apache Spark can be deployed on a Stand alone or on Hadoop or on Mesos.
Apache spark by default uses File System store. It works HDFS, Apache Cassandra, S3 and may be other storage systems.

###Spark Eco System
Spark Eco System has several libraries that provides additional capabilities. Some of the libraries are

* Spark Streaming: used for near real time processing of data. It uses stream of RDD's for processing the data
* Spark SQL: Provides capability to expose datasets over SQL queries
* Spark ML Lib: a scalable Machine Learning Library with commpin machine learning alogorithms such as regression, classification, clustering, collaborative filtering etc.
* Spark GraphX: API for grpahs and parallel computation. 

###Resilient Data Sets

Apache Spark relies heavily on the concept of RDD. RDD stands for Resilient Distributed Dataset. It provides a handle to individual data partitions which are the result of some computation.
It provides the basic abstraction for Data representation for Data processing

RDD(Resilient Distributed Dataset) is the key Class in the Apache Spark framework.

RDD provides a collection interface, which gives power to manipulate data, like counts, max, min, group by etc.
RDD can be cached to provide boost to performance.

SparkContext is available as part of the shell.
SparkContext can create a RDD from local files, external data sources like HDFS, database table like JDBC etc.
SparkConntext has lot of methods and most used one is the one to create an RDD. RDD is sparks abstraction for collection data distributed over the cluser.
RDD is lazily evaluated and immutable.
RDD provides transformations and operations. Transformantions gives a new RDD and operations triggers the actual calculations.
RDD does not restrict to MapReduce paradigm. 

RDD when partitioned will be a collections of individual partitions, and can be on separate nodes on a cluster.
With RDD handle, one can perform computations and transformations on all partitions within the data.
Whenever a part of the RDD is lost, Spark can recover these RDD's using lineage information. 
The lineage inforamtion is stored in DAG(Directed acyclic graph) and referes to sequence of transformations resulting in the current/lost RDD.
RDD does not impose restirctions on kind of data that can be stored and the API's can handle arbitary data types.
Most often Spark worked with key value pairs and hence Spark RDD is extended to supported additional functions using PairRDDFunctions, which expllicitly work on paired RDD functions.

###Installation
The tutorial uses  Apache Spark 1.4.1
* The following are the requisites.
* Ubuntu 12 or 14
* Apache Spark Installation
* Open JDK 1.7
* Scala 2.11.7
* Python 2.7.3 for PySpark

Download Spark from the following URL <a href="http://spark.apache.org/downloads.html">Spark Downloads</a>
Choose Package Type as "Pre-built for Hadoop 2.6 and later"


A quick example
Invoking the spark-shell command.

```
cd SPARK_HOME (go to the installation directory of spark)
bin/spark-shell
```

```
scala> val data = Array(1, 2, 3, 4, 5)
data: Array[Int] = Array(1, 2, 3, 4, 5)
scala> val rddData = sc.parallelize(data)
```

####Development Environment with Eclipse
FIX
```
sbt eclipse
```

##Getting Started


###Map
Map applies transformation function on each of the items in the RDD. The return value is also an RDD
####example 1

```
val fruits = sc.parallelize(List("orange", "apple", "kiwi", "kiwi", "rabbit", "avakado","mango", "grapes", "banana"), 3)
val lengths = fruits.map(_.length)
val fruit_lengths = fruits.zip(lengths)
fruit_lengths.collect
```

####example 2

```
val names = sc.parallelize(List("Peter","Paul","Mary","John","Harry", 2)
names.map(_.toUppercase)
val fruit_lengths = fruits.zip(lengths)
fruit_lengths.collect
```

###Folds
Reduces the given input. 

```
def reduce(f: (T, T) => T): T
```

####example 2

```
val numbers = sc.parallelize(1 to 100, 3)
numbers.reduce( _ + _ )
res0: Int = 5050
```

####example 2

```
val numbers = sc.parallelize(1 to 100, 3)
numbers.reduce( (x,y)=> x + y )
res1: Int = 5050
```

x is the previous value, and y is the current value. x+y is the cumulative sum of the numbers. The reduce takes a function, which shoud be commutative, other wise, reduce will give different results every time reduce is run on the same data

###ReduceByKey - tuples
Reduces the given input. 

```
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

val views_counts = views.map{case (country, month, program, likes, mins) => ((country,program),(likes, mins) )}.reduceByKey((x,y)=>((x._1+y._1),(x._2+y._2))).collect

views_counts: Array[((String, String), (Int, Int))] = Array(((India,The Robot),(220,2128)), ((US,BreakingBad),(500,5002)), ((US,News),(100,300)), ((India,Friends),(132,518)), ((India,BruceLee),(122,488)), ((US,Friends),(152,1530)), ((India,BreakingBad),(422,1266)), ((US,The Robot),(134,1193))
```

How it works
The first step is to defnine a map that returns tuples.
A key-value tuple is defined where key is also a tuple containing country and program. The value is also a tuple with likes and views.

```
views.map{case (country, month, program, likes, mins) => ((country,program),(likes, mins) )}
The next step is to reduce values by key.
The reduce function reduces the two values. x being the previus values and y being the current values. x and y are tuples, each containing (country,program),(likes, mins).
Reduce is an associative operation and it works by adding two values first, and then take next set of values and keep adding till all the records are finished.

```
reduceByKey((x,y)=>((x._1+y._1),(x._2+y._2))
```

###groupBy

```
scala> case class Item(id:String, name:String, unit:Int, companyId:String)

scala> case class Company(companyId:String, name:String, city:String)

scala> val i1 = Item("1", "first", 2, "c1")

scala> val i2 = i1.copy(id="2", name="second")

scala> val i3 = i1.copy(id="3", name="third", companyId="c2")

scala> val items = sc.parallelize(List(i1,i2,i3))
items: org.apache.spark.rdd.RDD[Item] = ParallelCollectionRDD[14] at parallelize at <console>:20

scala> val c1 = Company("c1", "company-1", "city-1")

scala> val c2 = Company("c2", "company-2", "city-2")

scala> val companies = sc.parallelize(List(c1,c2))

scala> val groupedItems = items.groupBy( x => x.companyId) 
groupedItems: org.apache.spark.rdd.RDD[(String, Iterable[Item])] = ShuffledRDD[16] at groupBy at <console>:22

scala> val groupedComp = companies.groupBy(x => x.companyId)
groupedComp: org.apache.spark.rdd.RDD[(String, Iterable[Company])] = ShuffledRDD[18] at groupBy at <console>:20

scala> groupedItems.join(groupedComp).take(10).foreach(println)

14/12/12 00:52:32 INFO DAGScheduler: Job 5 finished: take at <console>:35, took 0.021870 s
(c1,(CompactBuffer(Item(1,first,2,c1), Item(2,second,2,c1)),CompactBuffer(Company(c1,company-1,city-1))))
(c2,(CompactBuffer(Item(3,third,2,c2)),CompactBuffer(Company(c2,company-2,city-2))))
```

###Multi Columns Map/Reduce with Apache Spark

```
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
```

###Aggregate

```
val z = sc.parallelize(List(1,2,3,4,5,6), 2)
z.aggregate(0)(_+_,_+_)

def aggregate[U](zeroValue: U)(seqOp: (U, T) => U, combOp: (U, U) => U)(implicit scala.reflect.ClassTag[U]): U 
(Fist operation is applied on each partition and second opertion is applied on the result aggregates)

def myfunc(index: Int, iter:Iterator[Int]) : Iterator[String] = {
	iter.toList.map(x=>"[partid:" + index +  ",val:" +  x + "]").iterator
}

z.mapPartitionsWithIndex(myfunc).collect

res2: Array[String] = Array([partid:0,val:1], [partid:0,val:2], [partid:0,val:3], [partid:1,val:4], [partid:1,val:5], [partid:1,val:6])

z.aggregate(0)(math.max(_,_),_+_)
z.mapPartitionsWithIndex( (index: Int, it: Iterator[Int]) =>it.toList.map(x =>  if(index == 1) {x}).iterator).collect
```

###MapPartitionWithIndex
Printing values with iterator.

```
val data = 1 to 50
val distData = sc.parallelize(data,10)
distData.mapPartitionsWithIndex( (index: Int, it: Iterator[Int]) =>it.toList.map(x => if (index == 5 ) {Some(x)}).iterator).collect

val z2 = sc.parallelize(List("1","12","23","345","4567"),2)
z2.aggregate("")((x,y) => math.max(x.length, y.length).toString, (x,y) => x + y)
res141: String = 42


val z5 = sc.parallelize(List("1","12","23","345","4567"),2)
z5.mapPartitionsWithIndex( (index: Int, it: Iterator[String]) =>it.toList.map(x =>  if (index == 0) {println(x)}).iterator).collect
z5.aggregate("")((x,y) => math.min(x.length, y.length).toString, (x,y) => x + y)


z4.aggregate("")((x,y) => math.min(x.length, y.length).toString, (x,y) => x + y)
res141: String = 11 -- seems to be a problem
```

###SparkSQL and Join

```
object SparkSQLJoin {

case class Item(id:String, name:String, unit:Int, companyId:String)
case class Company(companyId:String, name:String, city:String)

def main(args: Array[String]) {

    val sparkConf = new SparkConf()
    val sc= new SparkContext(sparkConf)
    val sqlContext = new SQLContext(sc)

    import sqlContext.createSchemaRDD

    val i1 = Item("1", "first", 1, "c1")
    val i2 = Item("2", "second", 2, "c2")
    val i3 = Item("3", "thied", 3, "c3")
    val c1 = Company("c1", "company-1", "city-1")
    val c2 = Company("c2", "company-2", "city-2")

    val companies = sc.parallelize(List(c1,c2))
    companies.registerAsTable("companies")

    val items = sc.parallelize(List(i1,i2,i3))
    items.registerAsTable("items")

    val result = sqlContext.sql("SELECT * FROM companies C JOIN items I ON C.companyId= I.companyId").collect

    result.foreach(println)

    }
}

val mappedItems = items.map(item => (item.companyId, item))
val mappedComp = companies.map(comp => (comp.companyId, comp))
mappedItems.join(mappedComp).take(10).foreach(println)

(c1,(Item(1,first,2,c1),Company(c1,company-1,city-1)))
(c1,(Item(2,second,2,c1),Company(c1,company-1,city-1)))
(c2,(Item(3,third,2,c2),Company(c2,company-2,city-2)))

res5: Array[(Int, (String, String))] = Array((10,(jordan,hadoop)), (20,(ricky,spark)), (30,(matt,hive)), (30,(rhonda,hive)))

val emp = sc.parallelize(Seq((1,"jordan",10), (2,"ricky",20), (3,"matt",30), (4,"mince",35), (5,"rhonda",30)))

// Create dept RDD
val dept = sc.parallelize(Seq(("hadoop",10), ("spark",20), ("hive",30), ("sqoop",40)))

// Establishing that the third field is to be considered as the Key for the emp RDD
val manipulated_emp = emp.keyBy(t => t._3)

// Establishing that the second field need to be considered as the Key for dept RDD
val manipulated_dept = dept.keyBy(t => t._2)

// Inner Join
val join_data = manipulated_emp.join(manipulated_dept)

join_data: Array[(Int, ((Int, String, Int), (String, Int)))] = Array((10,((1,jordan,10),(hadoop,10))), (20,((2,ricky,20),(spark,20))), (30,((3,matt,30),(hive,30))), (30,((5,rhonda,30),(hive,30))))

val cleaned_joined_data = join_data.map(t => (t._2._1._1, t._2._1._2, t._1, t._2._2._1))


// Left Outer Join
val left_outer_join_data = manipulated_emp.leftOuterJoin(manipulated_dept)
// Right Outer Join
val right_outer_join_data = manipulated_emp.rightOuterJoin(manipulated_dept)
// Full Outer Join
val full_outer_join_data = manipulated_emp.fullOuterJoin(manipulated_dept)

// Formatting the Joined Data for better understandable (using map)
val cleaned_joined_data = join_data.map(t => (t._2._1._1, t._2._1._2, t._1, t._2._2._1))


val emp = sc.parallelize(Seq(("jordan",10), ("ricky",20), ("matt",30), ("mince",35), ("rhonda",30)))
val dept = sc.parallelize(Seq(("hadoop",10), ("spark",20), ("hive",30), ("sqoop",40)))

val shifted_fields_emp = emp.map(t => (t._2, t._1))
val shifted_fields_dept = dept.map(t => (t._2,t._1))

shifted_fields_emp.join(shifted_fields_dept)

```

###Joining two csv files with common join key 

```
val format = new java.text.SimpleDateFormat("yyyy-MM-dd")

case class Register (d: java.util.Date, uuid: String, cust_id: String, lat: Float, lng: Float)
case class Click (d: java.util.Date, uuid: String, landing_page: Int)

val reg = sc.textFile("reg.tsv").map(_.split("\t")).map(
 r => (r(1), Register(format.parse(r(0)), r(1), r(2), r(3).toFloat, r(4).toFloat))
)

reg.take(2)
res19: Array[(String, Register)] = Array((15dfb8e6cc4111e3a5bb600308919594,Register(Fri Mar 02 00:00:00 IST 14,15dfb8e6cc4111e3a5bb600308919594,1,33.659943,-117.95812)), (81da510acc4111e387f3600308919594,Register(Tue Mar 04 00:00:00 IST 2014,81da510acc4111e387f3600308919594,2,33.85701,-117.85574)))

val clk = sc.textFile("clk.tsv").map(_.split("\t")).map(
 c => (c(1), Click(format.parse(c(0)), c(1), c(2).trim.toInt))
)
clk.take(2)
res18: Array[(String, Click)] = Array((15dfb8e6cc4111e3a5bb600308919594,Click(Tue Mar 04 00:00:00 IST 2014,15dfb8e6cc4111e3a5bb600308919594,11)), (81da510acc4111e387f3600308919594,Click(Thu Mar 06 00:00:00 IST 2014,81da510acc4111e387f3600308919594,61)))


reg.join(clk).take(2)
res17: Array[(String, (Register, Click))] = Array((81da510acc4111e387f3600308919594,(Register(Tue Mar 04 00:00:00 IST 2014,81da510acc4111e387f3600308919594,2,33.85701,-117.85574),Click(Thu Mar 06 00:00:00 IST 2014,81da510acc4111e387f3600308919594,61))), (15dfb8e6cc4111e3a5bb600308919594,(Register(Fri Mar 02 00:00:00 IST 14,15dfb8e6cc4111e3a5bb600308919594,1,33.659943,-117.95812),Click(Tue Mar 04 00:00:00 IST 2014,15dfb8e6cc4111e3a5bb600308919594,11))))

```

###Joining and filtering data from two data sets 

####method 1

```
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

```

####method 2
val wc1 = sc.textFile("README.md").

```
flatMap(line => line.split(" ")).
map(word => (word, 1))
val wc2 = sc.textFile("docs/contributing-to-spark.md").
flatMap(line => line.split(" ")).
map(word => (word, 1))
wc1.union(wc2).
reduceByKey(_ + _).
filter(_._1 == "Spark").
collect()
```

####method3

```
sc.textFile("README.md").
union(sc.textFile("docs/contributing-to-spark.md")).
flatMap(_.split(" ")).
filter(_ == "Spark").
count()
res2: Long = 20
```

###Writing into a File
             
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
```

###WordCount

A simple word count example is shown below:

```
val input = sparkContext.textFile("path/to/input/file")
val words = input.flatMap(line => line.split(" "))
val wordsMappedToOne = words.map(word => (word, 1))
val wordOccrCount = wordsMappedToOne.reduceByKey((a, b) => a + b)
wordOccrCount.saveAsTextFile("path/to/output/file")
```


##Scala Spark examples

Calculate number of Lines in which character a and b occur in a text file

####Simple Scala App
Source Code

package basic

```
import org.apache.spark.SparkContext
import org.apache.spark.SparkContext._
import org.apache.spark.SparkConf

object SimpleApp {
def main(args: Array[String]) {
val logFile = "/home/ubuntu/work/spark/spark-1.3.0-bin-hadoop2.4/README.md" // Should be some file on your system
val conf = new SparkConf().setAppName("Simple Application")
val sc = new SparkContext(conf)
val logData = sc.textFile(logFile, 2).cache()
val numAs = logData.filter(line => line.contains("a")).count()
val numBs = logData.filter(line => line.contains("b")).count()
println("Lines with a: %s, Lines with b: %s".format(numAs, numBs))
}
}
````

####Compiling

sbt package
Execute the Code

```
~/work/spark/spark-1.3.0-bin-hadoop2.4/bin/spark-submit  \
--class "basic.SimpleApp"   --master local[4]   target/scala-2.10/ml-project_2.10-1.0.jar
Output
```

```
15/04/11 07:04:47 INFO TaskSetManager: Finished task 0.0 in stage 1.0 (TID 2) in 21 ms on localhost (1/2)
15/04/11 07:04:47 INFO DAGScheduler: Stage 1 (count at SimpleApp.scala:12) finished in 0.023 s
15/04/11 07:04:47 INFO DAGScheduler: Job 1 finished: count at SimpleApp.scala:12, took 0.046370 s
    15/04/11 07:04:47 INFO TaskSetManager: Finished task 1.0 in stage 1.0 (TID 3) in 21 ms on localhost (2/2)
    15/04/11 07:04:47 INFO TaskSchedulerImpl: Removed TaskSet 1.0, whose tasks have all completed, from pool
    Lines with a: 60, Lines with b: 29
```

####Word Count in Spark Scala

Source

package basic

import org.apache.spark.SparkContext
    import org.apache.spark.SparkContext._
    import org.apache.spark.SparkConf

    object WordCount {
      def main(args: Array[String]) {
        val file = "/home/ubuntu/work/spark/spark-1.3.0-bin-hadoop2.4/README.md" // Should be some file on your system
        val conf = new SparkConf().setAppName("Word Count")
        val sc = new SparkContext(conf)
        val lines = sc.textFile(file, 2).cache()
        val words = files.flapMap(line => line.split(" "))


      }
    }
Compile the code

sbt package
Execute the Code

~/work/spark/spark-1.3.0-bin-hadoop2.4/bin/spark-submit --class \
  "basic.WordCount" --master local[4] target/scala-2.10/ml-project_2.10-1.0.jar





####Getting started with Cassandra
Preparing example Cassandra schema
Create a simple keyspace and table in Cassandra. Run the following statements in cqlsh:

```
CREATE KEYSPACE test WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1 };
CREATE TABLE test.kv(key text PRIMARY KEY, value int);
Then insert some example data:

INSERT INTO test.kv(key, value) VALUES ('key1', 1);
INSERT INTO test.kv(key, value) VALUES ('key2', 2);
```

Now you're ready to write your first Spark program using Cassandra.
Setting up SparkContext

Before creating the SparkContext, set the spark.cassandra.connection.host property to the address of one of the Cassandra nodes:


```
val conf = new SparkConf(true)
   .set("spark.cassandra.connection.host", "127.0.0.1")
```

####Scala: Machine Learning

MLlib is Spark’s library of machine learning functions. Designed to run in parallel on clusters, MLlib contains a variety of learning algorithms and is accessible from all of Spark’s programming languages.

MLlib’s design and philosophy are simple: it lets you invoke various algorithms on distributed datasets, representing all data as RDDs. MLlib introduces a few data types (e.g., labeled points and vectors), but at the end of the day, it is simply a set of functions to call on RDDs.

Logistical Regression with SGD

This program uses two MLlib algorithms: HashingTF, which builds term frequency feature vectors from text data, and Logistic RegressionWithSGD, which implements the logistic regression procedure using stochastic gradient descent (SGD)

import org.apache.spark.SparkContext
import org.apache.spark.SparkContext._
import org.apache.spark.SparkConf
import org.apache.spark.mllib.regression.LabeledPoint
import org.apache.spark.mllib.feature.HashingTF
import org.apache.spark.mllib.classification.LogisticRegressionWithSGD

object SpamFilter {
        def main(args: Array[String]) {
        val conf = new SparkConf().setAppName("SpamFilter")
        val sc = new SparkContext(conf)
        val home = "/home/ubuntu/work/spark/spark-samples/"
        val spam = sc.textFile(home + "ml-samples/data/spam_v1_text.txt")
        val normal = sc.textFile(home + "ml-samples/data/non-spam_v1_text.txt")

        // Create a HashingTF instance to map email text to
        // vectors of 10,000 features.
        val tf = new HashingTF(numFeatures = 10000)
        // Each email is split into words,
        //and each word is mapped to one feature.
        val spamFeatures = spam.map(email => tf.transform(email.split(" ")))
        val normalFeatures = normal.map(email => tf.transform(email.split(" ")))

        // Create LabeledPoint datasets for positive (spam)
        // and negative (normal) examples.
        val positiveExamples = spamFeatures.map(
    features => LabeledPoint(1, features))
        val negativeExamples = normalFeatures.map(
    features => LabeledPoint(0, features))
        val trainingData = positiveExamples.union(negativeExamples)
        // Cache since Logistic Regression is an iterative algorithm.
        trainingData.cache()

        // Run Logistic Regression using the SGD algorithm.
        val model = new LogisticRegressionWithSGD().run(trainingData)

        // Test on a positive example (spam) and a negative one (normal).
        val sOne = "iPhone Leather Sleeve CASSIOPEIA http://t.co/EMtxZNU2ro | " +
                        "#iphone #iphone5 #iPhone5Sleeve #iPhoneSleeve " +
                        "#iPhone5sSleeve #iPhone5s #Swarovski"
        val sTwo = "this is non spam text "
        val sThree = "@airtelghana  thank you soo much #iphone5s​"
        val posTest = tf.transform(sOne.split(" "))
        val negTest = tf.transform(sTwo.split(" "))
        val thirdTest = tf.transform(sThree.split(" "))
        println("Prediction for Spam '" + sOne  + "' : "+ model.predict(posTest))
        println("Prediction for spam '" + sTwo + "' : " + model.predict(negTest))
        println("Prediction for spam '" + sThree + "' :  " + model.predict(thirdTest))
  }
}
Execute the Code

~/work/spark/spark-1.3.0-bin-hadoop2.4/bin/spark-submit --class \
  "ml.SpamFilter" --master local[4] target/scala-2.10/ml-project_2.10-1.0.jar
TF-IDF Sample

object TfIdfSample{
  def main(args: Array[String]) {
        val file = "/home/ubuntu/work/spark/spark-samples/ml-samples/data/README.md"
        val conf = new SparkConf().setAppName("TfIdfSample")
        val sc = new SparkContext(conf)
        val documents: RDD[Seq[String]] = sc.textFile(file).map(_.split(" ").toSeq)
        print("Documents Size:" + documents.count)
        val hashingTF = new HashingTF()
        val tf = hashingTF.transform(documents)
        for(tf_ <- tf) {
          println(s"$tf_")
        }
        tf.cache()
        val idf = new IDF().fit(tf)
        val tfidf = idf.transform(tf)
        println("tfidf size : " + tfidf.count)
        for(tfidf_ <- tfidf) {
          println(s"$tfidf_")
        }
  }
}
Execute the Code

~/work/spark/spark-1.3.0-bin-hadoop2.4/bin/spark-submit --class \
  "ml.TfIdfSample" --master local[4] target/scala-2.10/ml-project_2.10-1.0.jar
Word2Vector Sample

Word2Vec computes distributed vector representation of words. The main advantage of the distributed representations is that similar words are close in the vector space, which makes generalization to novel patterns easier and model estimation more robust.

object Word2Vector{
  def main(args: Array[String]) {
        val file = "/home/ubuntu/work/spark/spark-samples/ml-samples/data/text8_10000"
        val conf = new SparkConf().setAppName("Word2Vector")
        val sc = new SparkContext(conf)
        val input = sc.textFile(file).map(line => line.split(" ").toSeq)
        val word2vec = new Word2Vec()
        val model = word2vec.fit(input)
        val synonyms = model.findSynonyms("anarchist", 40)
        for((synonym, cosineSimilarity) <- synonyms) {
          println(s"$synonym $cosineSimilarity")
        }
  }
}
Hashing TF Sample

object HashingTFSample{
  def main(args: Array[String]) {
        val conf = new SparkConf().setAppName("SpamFilter")
        val sc = new SparkContext(conf)
        val sentence = "This is a simple text"
        val words = sentence.split(" ")
        val tf = new HashingTF(numFeatures = 10000)
        val sparseVector = words.map(w => tf.transform(w))
        for(sv <- sparseVector) {
          println(s"$sv")
        }
  }
}
Consine Similarity

Input Data

            0 2.857738033247042 0 2.061393766919624 2.619965104088255 4.745052855503306 2.004684436494304 0 2.122974378789621 2.228387042742021 2.228387042742023 0 0 0 0 0 0
    0 2.857738033247042 0 0 0 0 2.004684436494304 2.000347299268466 0 2.228387042742021 2.228387042742023 0 2.055002875864414 0 0 0 0
    1 0 2.52078447201548 2.061393766919624 0 0 2.004684436494304 2.000347299268466 0 0 0 0 2.055002875864414 0 0 0 0
    0 2.857738033247042 0 2.061393766919624 0 0 0 0 2.122974378789621 2.228387042742021 2.228387042742023 0 2.055002875864414 0 0 0 0
    0 2.857738033247042 0 0 2.619965104088255 0 2.004684436494304 2.000347299268466 0 2.228387042742021 2.228387042742023 0 0 0 0 0 0
    1 0 0 0 2.619965104088255 0 2.004684436494304 2.000347299268466 0 2.228387042742021 2.228387042742023 0 0 0 0 0 0
    1 2.857738033247042 2.52078447201548 2.061393766919624 2.619965104088255 0 2.004684436494304 0 0 2.228387042742021 2.228387042742023 0 0 0 0 0 0
    1 2.857738033247042 2.52078447201548 2.061393766919624 2.619965104088255 0 2.004684436494304 2.000347299268466 0 0 0 0 0 0 0 0 0
    1 2.857738033247042 0 2.061393766919624 2.619965104088255 0 0 2.000347299268466 0 0 0 0 2.055002875864414 0 0 0 0
...
object CosineSimilarity{
  def main(args: Array[String]) {
        val file = "/home/ubuntu/work/spark/spark-samples/ml-samples/data/sample_svm_data.txt"
        val conf = new SparkConf().setAppName("CosineSimilarity")
        val threshold = 0.1
        val sc = new SparkContext(conf)

        // Load and parse the data file.
        val rows = sc.textFile(file).map { line =>
          val values = line.split(' ').map(_.toDouble)
          Vectors.dense(values)
        }.cache()
        val mat = new RowMatrix(rows)

        // Compute similar columns perfectly, with brute force.
        val exact = mat.columnSimilarities()

        // Compute similar columns with estimation using DIMSUM
        val approx = mat.columnSimilarities(threshold)

        val exactEntries = exact.entries.map { case MatrixEntry(i, j, u) => ((i, j), u) }
        val approxEntries = approx.entries.map { case MatrixEntry(i, j, v) => ((i, j), v) }
        val MAE = exactEntries.leftOuterJoin(approxEntries).values.map {
          case (u, Some(v)) =>
            math.abs(u - v)
          case (u, None) =>
            math.abs(u)
        }.mean()

        println(s"Average absolute error in estimate is: $MAE")

        sc.stop()
  }
}
Convert Word to Vectors

object ConvertWordsToVectors{
  def main(args: Array[String]) {
        val file = "/home/ubuntu/work/spark/spark-samples/ml-samples/data/text8_10000"
        val conf = new SparkConf().setAppName("Word2Vector")
        val sc = new SparkContext(conf)
        val input = sc.textFile(file).map(line => line.split(" ").toSeq)
        val word2vec = new Word2Vec()
        val model = word2vec.fit(input)
        val vectors = model.getVectors
        vectors foreach ( (t2) => println (t2._1 + "-->" + t2._2.mkString(" ")))
  }
}



#Scala: Spark-Sql

Create DataFrame From Json

{"name":"Michael"}
{"name":"Andy", "age":30}
{"name":"Justin", "age":19}
object CreateDataFrame {
        def main(args: Array[String]) {
                val dataFile =
        "/home/ubuntu/work/spark-src/spark/examples/src/main/resources/people.json"
                val conf = new SparkConf().setAppName("Simple Application")
                val sc = new SparkContext(conf)
                val sqlContext = new org.apache.spark.sql.SQLContext(sc)
        val df = sqlContext.jsonFile(dataFile)
        df.show()
        }
}



####DataFrame Operations

Print the schema in a tree format

df.printSchema()
Select only the “name” column

df.select("name").show()
// name
// Michael
// Andy
// Justin
Select everybody, but increment the age by 1

df.select(df("name"), df("age") + 1).show()
// name    (age + 1)
// Michael null
// Andy    31
// Justin  20
Select people older than 21

df.filter(df("age") > 21).show()
// age name
// 30  Andy
Count people by age

df.groupBy("age").count().show()
// age  count
// null 1
// 19   1
// 30   1
Complete Listing

object DataFrameOperations {
        def main(args: Array[String]) {
                val dataFile =
                        "/home/ubuntu/work/spark-src/spark/" +
                        "examples/src/main/resources/people.txt"
                val conf = new SparkConf().setAppName("DataFrameOperations")
                val sc = new SparkContext(conf)
                val sqlContext = new org.apache.spark.sql.SQLContext(sc)
                val df = sqlContext.jsonFile(dataFile)
                df.show()
                // Print the schema in a tree format
                df.printSchema()

                // Select only the "name" column
                df.select("name").show()

                // Select everybody, but increment the age by 1
                df.select(df("name"), df("age") + 1).show()

                // Select people older than 21
                df.filter(df("age") > 21).show()

                // Count people by age
                df.groupBy("age").count().show()
        }
}



####Programmatic Schema

object ProgrammaticSchema {
        def main(args: Array[String]) {
                val dataFile = "/home/ubuntu/work/spark-src/spark/" +
                                                "examples/src/main/resources/people.txt"
                val conf = new SparkConf().setAppName("ProgrammaticSchema")
                val sc = new SparkContext(conf)
                val people = sc.textFile(dataFile)

                  val sqlContext = new org.apache.spark.sql.SQLContext(sc)
                val schemaString = "name age"
                val schema = StructType(schemaString.split(" ").
                        map(fieldName => StructField(fieldName, StringType, true)))

                // Convert records of the RDD (people) to Rows.
                val rowRDD = people.map(_.split(",")).map(p => Row(p(0), p(1).trim))
                val peopleDataFrame = sqlContext.createDataFrame(rowRDD, schema)

                // Register the DataFrames as a table.
                peopleDataFrame.registerTempTable("people")

                // SQL statements can be run by using the sql methods provided by sqlContext.
                val results = sqlContext.sql("SELECT name FROM people")

                // The results of SQL queries are DataFrames and support all
                // the normal RDD operations.
                // The columns of a row in the result can be accessed by ordinal.
                results.map(t => "Name: " + t(0)).collect().foreach(println)
        }
}



####Store DataFrame as ParquetFile

object StoreParquet {
        def main(args: Array[String]) {
                val dataFile =
                  "/home/ubuntu/work/spark-src/spark/examples/" +
                  "src/main/resources/people.txt"
                val conf = new SparkConf().setAppName("StoreParquet")
                val sc = new SparkContext(conf)
                val people = sc.textFile(dataFile)
                val schemaString = "name age"
                val schema = StructType(schemaString.split(" ").map(
                        fieldName => StructField(fieldName, StringType, true)))

                val sqlContext = new org.apache.spark.sql.SQLContext(sc)
                val rowRDD = people.map(_.split(",")).map(p => Row(p(0), p(1).trim))
                val peopleDataFrame = sqlContext.createDataFrame(rowRDD, schema)
                peopleDataFrame.saveAsParquetFile("output/people.parquet")
  }
}
Execute the Code

~/work/spark/spark-1.3.0-bin-hadoop2.4/bin/spark-submit --class \
  "sql.StoreParquet" --master local[4] target/scala-2.10/ml-project_2.10-1.0.jar



###PySpark: WordCountPyspark

Part 1 : Creating a base RDD and pair RDDs

Based on Lab Exercises from https://courses.edx.org/courses/BerkeleyX/CS190.1x/1T2015/info

Create a base RDD

We’ll start by generating a base RDD by using a Python list and the sc.parallelize method. Then we’ll print out the type of the base RDD.

wordsList = ['cat', 'elephant', 'rat', 'rat', 'cat']
wordsRDD = sc.parallelize(wordsList, 4)
print wordsRDD.collect()
['cat', 'elephant', 'rat', 'rat', 'cat']
def makePlural(word):
    """Adds an 's' to `word`.
    Note:
        This is a simple function that only adds an 's'.  No attempt is made to follow proper
        pluralization rules.
    Args:
        word (str): A string.
    Returns:
        str: A string with 's' added to it.
    """
    return word + 's'
pluralRDD = wordsRDD.map(makePlural)
print pluralRDD.collect()
['cats', 'elephants', 'rats', 'rats', 'cats']
pluralLambdaRDD = wordsRDD.map(lambda x: x + 's')
print pluralLambdaRDD.collect()
['cats', 'elephants', 'rats', 'rats', 'cats']
** Length of each word **

Now use map() and a lambda function to return the number of characters in each word. We’ll collect this result directly into a variable.

pluralLengths = (pluralRDD
                 .map(len)
                 .collect())
print pluralLengths
[4, 9, 4, 4, 4]
Pair RDDs

The next step in writing our word counting program is to create a new type of RDD, called a pair RDD. A pair RDD is an RDD where each element is a pair tuple (k, v) where k is the key and v is the value. In this example, we will create a pair consisting of ('<word>', 1) for each word element in the RDD. We can create the pair RDD using the map() transformation with a lambda() function to create a new RDD.

wordPairs = wordsRDD.map(lambda x: (x,1))
print wordPairs.collect()
[('cat', 1), ('elephant', 1), ('rat', 1), ('rat', 1), ('cat', 1)]
** Part 2: Counting with pair RDDs **

Now, let’s count the number of times a particular word appears in the RDD. There are multiple ways to perform the counting, but some are much less efficient than others. A naive approach would be to collect() all of the elements and count them in the driver program. While this approach could work for small datasets, we want an approach that will work for any size dataset including terabyte- or petabyte-sized datasets. In addition, performing all of the work in the driver program is slower than performing it in parallel in the workers. For these reasons, we will use data parallel operations.

**groupByKey() approach ** An approach you might first consider (we’ll see shortly that there are better ways) is based on using the groupByKey() transformation. As the name implies, the groupByKey() transformation groups all the elements of the RDD with the same key into a single list in one of the partitions. There are two problems with using groupByKey():

The operation requires a lot of data movement to move all the values into the appropriate partitions.

The lists can be very large. Consider a word count of English Wikipedia: the lists for common words (e.g., the, a, etc.) would be huge and could exhaust the available memory in a worker.

Use groupByKey() to generate a pair RDD of type ('word', iterator).

wordsGrouped = wordPairs.groupByKey()
for key, value in wordsGrouped.collect():
    print '{0}: {1}'.format(key, list(value))
rat: [1, 1]
elephant: [1]
cat: [1, 1]
**Use groupByKey() to obtain the counts ** Using the groupByKey() transformation creates an RDD containing 3 elements, each of which is a pair of a word and a Python iterator. Now sum the iterator using a map() transformation. The result should be a pair RDD consisting of (word, count) pairs.

wordCountsGrouped = wordsGrouped.map(lambda (k, v): (k, sum(v)))
print wordCountsGrouped.collect()
[('rat', 2), ('elephant', 1), ('cat', 2)]
** Counting using reduceByKey **

A better approach is to start from the pair RDD and then use the reduceByKey() transformation to create a new pair RDD. The reduceByKey() transformation gathers together pairs that have the same key and applies the function provided to two values at a time, iteratively reducing all of the values to a single value. reduceByKey() operates by applying the function first within each partition on a per-key basis and then across the partitions, allowing it to scale efficiently to large datasets.

wordCounts = wordPairs.reduceByKey(lambda x, y: x+ y)
print wordCounts.collect()
[('rat', 2), ('elephant', 1), ('cat', 2)]
** All together ** The expert version of the code performs the map() to pair RDD, reduceByKey() transformation, and collect in one statement.

wordCountsCollected = (wordsRDD
                       .map(lambda x: (x,1))
                       .reduceByKey(lambda x, y: x+ y)
                       .collect())
print wordCountsCollected
print wordsRDD
[('rat', 2), ('elephant', 1), ('cat', 2)]
ParallelCollectionRDD[0] at parallelize at PythonRDD.scala:396
Part 3: Finding unique words and a mean value

** Unique words ** Calculate the number of unique words in wordsRDD. You can use other RDDs that you have already created to make this easier.

uniqueWords =  wordsRDD.distinct().count()
print uniqueWords
3
** Mean using reduce ** Find the mean number of words per unique word in wordCounts. Use a reduce() action to sum the counts in wordCounts and then divide by the number of unique words. First map() the pair RDD wordCounts, which consists of (key, value) pairs, to an RDD of values.

from operator import add
totalCount = (wordCounts
            .map(lambda (key, val): val)
             .reduce(add))
average = totalCount / float(uniqueWords)
print totalCount
print round(average, 2)
5
1.67
Part 4: Apply word count to a file

In this section we will finish developing our word count application. We’ll have to build the wordCount function, deal with real world problems like capitalization and punctuation, load in our data source, and compute the word count on the new data.

** WordCount function **

First, define a function for word counting. You should reuse the techniques that have been covered in earlier parts of this lab. This function should take in an RDD that is a list of words like wordsRDD and return a pair RDD that has all of the words and their associated counts.

def wordCount(wordListRDD):
    """Creates a pair RDD with word counts from an RDD of words.
    Args:
        wordListRDD (RDD of str): An RDD consisting of words.
    Returns:
        RDD of (str, int): An RDD consisting of (word, count) tuples.
    """
    return (wordListRDD.map(lambda x: (x,1)).reduceByKey(lambda x, y: x+y))

print wordCount(wordsRDD).collect()
[('rat', 2), ('elephant', 1), ('cat', 2)]
** Capitalization and punctuation **

Real world files are more complicated than the data we have been using in this lab. Some of the issues we have to address are: Words should be counted independent of their capitialization (e.g., Spark and spark should be counted as the same word). All punctuation should be removed. Any leading or trailing spaces on a line should be removed.

Define the function removePunctuation that converts all text to lower case, removes leading and trailing spaces, and removes any punctuation. Use the Python re module to remove any text that is not a letter, number, or space. Reading help(re.sub) might be useful.

import re
def removePunctuation(text):
    """Removes punctuation, changes to lowercase, and strips leading and trailing spaces.
    Note:
        Only spaces, letters, and numbers should be retained.  Other characters should should be
        eliminated. (e.g. it's becomes its)
    Args:
        text (str): A string.
    Returns:
        str: The cleaned up string.
    """
    return re.sub('[^a-z| |0-9]', '', text.strip().lower())
print removePunctuation("The Elephant's 4 cats. ")
the elephants 4 cats
** Load a text file **

For the next part of this lab, we will use the Complete Works of William Shakespeare from Project Gutenberg. To convert a text file into an RDD, we use the SparkContext.textFile() method. We also apply the recently defined removePunctuation() function using a map() transformation to strip out the punctuation and change all text to lowercase. Since the file is large we use take(15), so that we only print 15 lines.

Just run this code

import os.path
baseDir = os.path.join('data')
inputPath = os.path.join('cs100', 'lab1', 'shakespeare.txt')
fileName = "/home/ubuntu/work/spark/spark-data/shakespeare.txt"
shakespeareRDD = (sc
                  .textFile(fileName, 8)
                  .map(removePunctuation))
print '\n'.join(shakespeareRDD
                .zipWithIndex()  # to (line, lineNum)
                .map(lambda (l, num): '{0}: {1}'.format(num, l))  # to 'lineNum: line'
                .take(15))
0: the project gutenberg ebook of the complete works of william shakespeare by
1: william shakespeare
2:
3: this ebook is for the use of anyone anywhere at no cost and with
4: almost no restrictions whatsoever  you may copy it give it away or
5: reuse it under the terms of the project gutenberg license included
6: with this ebook or online at wwwgutenbergorg
7:
8:  this is a copyrighted project gutenberg ebook details below
9:      please follow the copyright guidelines in this file
10:
11: title the complete works of william shakespeare
12:
13: author william shakespeare
14:
Words from lines

Before we can use the wordcount() function, we have to address two issues with the format of the RDD: The first issue is that that we need to split each line by its spaces. The second issue is we need to filter out empty lines.

Apply a transformation that will split each element of the RDD by its spaces. For each element of the RDD, you should apply Python’s string split() function. You might think that a map() transformation is the way to do this, but think about what the result of the split() function will be.

shakespeareWordsRDD = shakespeareRDD.flatMap(lambda x: x.split(' '))
shakespeareWordCount = shakespeareWordsRDD.count()
print shakespeareWordsRDD.top(5)
print shakespeareWordCount
[u'zwaggerd', u'zounds', u'zounds', u'zounds', u'zounds']
950388
** Remove empty elements ** The next step is to filter out the empty elements. Remove all entries where the word is ''.

shakeWordsRDD = shakespeareWordsRDD.filter(lambda x: x != '')
shakeWordCount = shakeWordsRDD.count()
print shakeWordCount
903709



###Pyspark: Data Exploration

Interactive Analysis

Let’s now use Spark to do some order statistics on the data set. First, launch the Spark shell:

$ pyspark
>>>
The prompt should appear within a few seconds. Note: You may need to hit [Enter] once to clear the log output.

Warm up by creating an RDD (Resilient Distributed Dataset) named pagecounts from the input files. In the Spark shell, the SparkContext is already created for you as variable sc. Assuming the pyspark shell was launched from /home/ubuntu/work/spark-data.

>>> sc
<pyspark.context.SparkContext object at 0x7eff0eae95d0>

>>>pagecounts = sc.textFile('./pagecounts-20090505-20090506')
You can use the take operation of an RDD to get the first K records. Here, K = 10

>>> pagecounts.take(10)
This is not very readable because take() returns an array and Scala simply prints the array with each element separated by a comma. We can make it prettier by traversing the array to print each record on its own line.

>>> for x in pagecounts.take(10):
        print x
Output of the command is similar to listing below

20090505-000000 aa.b ?71G4Bo1cAdWyg 1 14463
20090505-000000 aa.b Special:Statistics 1 840
20090505-000000 aa.b Special:Whatlinkshere/MediaWiki:Returnto 1 1019
20090505-000000 aa.b Wikibooks:About 1 15719
20090505-000000 aa ?14mFX1ildVnBc 1 13205
20090505-000000 aa ?53A%2FuYP3FfnKM 1 13207
20090505-000000 aa ?93HqrnFc%2EiqRU 1 13199
20090505-000000 aa ?95iZ%2Fjuimv31g 1 13201
20090505-000000 aa File:Wikinews-logo.svg 1 8357
20090505-000000 aa Main_Page 2 9980
Let’s see how many records in total are in this data set (this command will take a while)

>>> pagecounts.count()
...
15/09/04 20:02:13 INFO DAGScheduler: Job 3 finished: count at <stdin>:1, took 9.495161 s
7812124
When your query finishes running, it should return the following count: 7812124

Let’s derive an RDD containing only English pages from pagecounts. This can be done by applying a filter function to pagecounts. For each record, we can split it by the field delimiter (i.e. a space) and get the second field-– and then compare it with the string “en”.

To avoid reading from disks each time we perform any operations on the RDD, we also cache the RDD into memory. This is where Spark really starts to to shine.

>>> enPages = pagecounts.filter(lambda x: x.split(" ")[1] == "en").cache()
How many records are there for English pages?

>>> enPages.count()
3357004

