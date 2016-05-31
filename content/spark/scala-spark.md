title: Big Data with Apache Spark
date: 2016-05-02
description: A tutorial on Apache Spark
tags: spark, programming, hadoop, bigdata, yarn


Calculate number of Lines in which character a and b occur in a text file

####Simple Scala App
Source Code

	:::scala
	package basic

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

####Compiling

sbt package
Execute the Code

	:::scala
	~/work/spark/spark-1.3.0-bin-hadoop2.4/bin/spark-submit  \
	--class "basic.SimpleApp"   --master local[4]   target/scala-2.10/ml-project_2.10-1.0.jar

Output

	:::text
	15/04/11 07:04:47 INFO TaskSetManager: Finished task 0.0 in stage 1.0 (TID 2) in 21 ms on localhost (1/2)
	15/04/11 07:04:47 INFO DAGScheduler: Stage 1 (count at SimpleApp.scala:12) finished in 0.023 s
	15/04/11 07:04:47 INFO DAGScheduler: Job 1 finished: count at SimpleApp.scala:12, took 0.046370 s
	    15/04/11 07:04:47 INFO TaskSetManager: Finished task 1.0 in stage 1.0 (TID 3) in 21 ms on localhost (2/2)
	    15/04/11 07:04:47 INFO TaskSchedulerImpl: Removed TaskSet 1.0, whose tasks have all completed, from pool
	    Lines with a: 60, Lines with b: 29

####Word Count in Spark Scala

Source

	:::scala
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

	:::scala
	~/work/spark/spark-1.3.0-bin-hadoop2.4/bin/spark-submit --class \
	  "basic.WordCount" --master local[4] target/scala-2.10/ml-project_2.10-1.0.jar

