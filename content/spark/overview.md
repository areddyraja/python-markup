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

![alt text](/static/images/spark/spark-overview.png)

* Spark Streaming: used for near real time processing of data. It uses stream of RDD's for processing the data
* Spark SQL: Provides capability to expose datasets over SQL queries
* Spark ML Lib: a scalable Machine Learning Library with common machine learning alogorithms such as regression, classification, clustering, collaborative filtering etc.
* Spark GraphX: API for grpahs and parallel computation.

###Spark Architecture overview


Spark provides the following main components(Apart from others)

* API
* Data Storage
* Resource Management

####API
Spark provides the API in each of these languages.
* Scala API
* Java API
* Python API

The Apis provide developers to create Spark Applications.

####Data Storage
Spark works seamlessly with Hadoop File Syste,(HDFS). It has connector to various different databases.
Cassndra Spark Connector connects to Cassandra for BiG Data Analyis.


####Resource Management
Spark cluster can work stand alone or can work with Yarn and Mesos.
Spark compute nodes are co-located with HDFS nodes or Cassandra nodes for Data Locality.

An overview of Job submission is shown below

![alt text](/static/images/spark/Spark-Job-submission.png)

The task is submitted to the Spark Cluster as shown below:

![alt text](/static/images/spark/task-schedule.png)

###Resilient Data Sets (RDDs)

Apache Spark relies heavily on the concept of RDD. RDD stands for Resilient Distributed Dataset. 
It provides a handle to individual data partitions which are the result of some computation.
It provides the basic abstraction for Data representation for Data processing


RDDs are

* Immutable in nature
* lazily evaluated
* cacheable

RDD(Resilient Distributed Dataset) is the key Class in the Apache Spark framework. 
They are fundamental to Apache Spark.

* RDD is array of reefernce partion objects
* Partiion is the basic unit of parralleism and each partition holds the subset of the data
* All partitions are assigned to the nodes in the cluster will follow data locality with minimum data transfer
* Partion is loaded into memory before partitioning
* RDD is lazily evaluated and immutable.
* RDD does not restrict to MapReduce paradigm. 
* RDD provides a collection interface, which gives power to manipulate data, like counts, max, min, group by etc.
* RDD can be cached to provide boost to performance.

RDDs can be created
* Using parallel collection object
* Creating RDD from external source like HDFS or FileSystem
* Executing any operation on an existing RDD

creation of RDD

	:::scala
	var fileRDD = sc.textFile(logFile) 

A new filtered RDD

	:::scala 
	var filteredRDD = fileRDD.filter(_.equals("FATAL")) 


SparkContext is available as part of the shell.
SparkContext can create a RDD from local files, external data sources like HDFS, database table like JDBC etc.
SparkConntext has lot of methods and most used one is the one to create an RDD. RDD is sparks abstraction for collection data distributed over the cluser.


* RDD when partitioned will be a collections of individual partitions, and can be on separate nodes on a cluster.
* With RDD handle, one can perform computations and transformations on all partitions within the data.
* Whenever a part of the RDD is lost, Spark can recover these RDD's using lineage information. 
* The lineage inforamtion is stored in DAG(Directed acyclic graph) and referes to sequence of transformations resulting in the current/lost RDD.
* RDD does not impose restirctions on kind of data that can be stored and the API's can handle arbitary data types.
* Most often Spark worked with key value pairs and hence Spark RDD is extended to supported additional functions using PairRDDFunctions, which expllicitly work on paired RDD functions.

RDD provides two basic operations

* Transformation
* Actions

#####Transformation Operations
Transformatins transform source RDD of one type to other RDD types.
Operarions like map, reduce, filter, flatMap are the operations.

Any transformation applied on RDD will give another RDD and will not perform the operation immediately.
It will create a DAG(Directed Acyclic Graph) using the applied operation, source RDD and function used for transformation.
The graph is built with all these operations till an action function is applied.

#####Action operations
This kind of operation gives another RDD, but will trigger the all the transformations that are built as the graph.
Operations like collect, count, first, saveAsTextFile are examples of Action operations.

	:::scala
	val logFile = "hdfs://master.backtobazics.com:9000/user/root/sample.txt"
	val lineRDD = sc.textFile(logFile)
Transformation 1 -> DAG created
{DAG: Start -> [sc.textFile(logFile)]}

	:::scala
	val wordRDD = lineRDD.flatMap(_.split(" ")) 
Transformation 2 -> wordRDD DAG updated

	:::scala
	{DAG: Start -> [sc.textFile(logFile)] 
            -> [lineRDD.flatMap(_.split(" "))]}

	val filteredWordRDD = wordRDD.filter(_.equalsIgnoreCase("the")) 

Transformation 3 -> filteredWordRDD DAG updated

	:::scala
	{DAG: Start -> [sc.textFile(logFile)] 
              -> [lineRDD.flatMap(_.split(" "))]
                -> [wordRDD.filter(_.equalsIgnoreCase("the"))]}


Action: collect
Execute DAG & collect result to driver node

	:::scala	
	filteredWordRDD.collect 

