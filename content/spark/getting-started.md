title: Apache Spark Getting Started
date: 2016-05-02
description: A tutorial on Apache Spark
tags: spark, programming, hadoop, bigdata, yarn

##Getting Started

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


####Interacting with Spark
Intercation with Spark can happen by using either spark-shell or pyspark.cmd

Invoking the spark-shell command.

	:::text
	cd $SPARK_HOME (go to the installation directory of spark)
	bin/spark-shell
 
Type the following:

	:::text
	scala> val data = Array(1, 2, 3, 4, 5)
	data: Array[Int] = Array(1, 2, 3, 4, 5)
	scala> val rddData = sc.parallelize(data)

####Spark Web Console
The Spark web console can be accessed using the following URL

	:::scala
	http://localhost:4040

####Development Environment with Eclipse
FIX THIS

```
sbt eclipse
```

###WordCount

A simple word count example is shown below:
Invoke Spark-Shell using ```bin/spark-shell``` and type the following code.

	:::scala
	val input = sparkContext.textFile("path/to/input/file")
	val words = input.flatMap(line => line.split(" "))
	val wordsMappedToOne = words.map(word => (word, 1))
	val wordOccrCount = wordsMappedToOne.reduceByKey((a, b) => a + b)
	wordOccrCount.saveAsTextFile("path/to/output/file")

