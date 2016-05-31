title: Big Data with Apache Spark
date: 2016-05-02
description: A tutorial on Apache Spark
tags: spark, programming, hadoop, bigdata, yarn

####Getting started with Cassandra
Preparing example Cassandra schema
Create a simple keyspace and table in Cassandra. Run the following statements in cqlsh:

	:::scala
	CREATE KEYSPACE test WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1 };
	CREATE TABLE test.kv(key text PRIMARY KEY, value int);
	Then insert some example data:

	INSERT INTO test.kv(key, value) VALUES ('key1', 1);
	INSERT INTO test.kv(key, value) VALUES ('key2', 2);

Now you're ready to write your first Spark program using Cassandra.
Setting up SparkContext

Before creating the SparkContext, set the spark.cassandra.connection.host property to the address of one of the Cassandra nodes:


	:::scala
	val conf = new SparkConf(true)
	   .set("spark.cassandra.connection.host", "127.0.0.1")


####Invoking Spark Shell

bin/spark-shell --master spark://172.31.18.36:7077  --jars /opt/spark-1.4.1-bin-hadoop2.6/lib/spark_cassandra_connector-assembly-1.0.0.jar 


