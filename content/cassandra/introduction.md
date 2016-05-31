



Cassandra belongs to a class of Key Value Databases. Its key is the partition key that identifies the row.
Cassandra is 

* Designed to handle large amount of data across multiple servers
* There is a lot of unorganized data out there
* Easy to implement and deploy
* Mimics traditional relational database systems, but with triggers and lightweight transactions
* Raw, simple data structures

Cassandra is 

* Scalable
* Open- source
* Suits for structured, semi-structured, unstructured data
* Schema-less: We can specify for adding a column at write time.

Cassandra has the following advantages

* perfect for time-series data
* high performance
* Decentralization
* nearly linear scalability
* replication support
* no single points of failure
* MapReduce support

Cassandra has the following disadvantages

* no referential integrity
* No concept of JOIN
* querying options for retrieving data are limited
* sorting data is a design decision
* no GROUP BY
* no support for atomic operations
* if operation fails, changes can still occur

Cassandra supports the following NoSQL properties

* ACID : General property of database systems   
* CAP: Little more about distributed systems
* BASE: Practical consideration of distributed systems

Cassandra is a decentralized system hence any node can serve your request.
OpsCenter is a  monitoring system which deals with cluster management and administration tasks.


#### Tunable Consistency
Cassandra suppots the following consistency levels

* ANY
* ONE
* QUORUM- Half of the nodes in replica+1
* LOCAL_QUORUM – Particular to one data center
* EACH_QUORUM – Like quorum on each data center

#### Data Modelling

* Primary key – It gives the cassandra storage system to distribute the data based on the value.
* When there are multiple fields in primary key, we refer it as compund key, in that the first key would be the primary and subsequent are clustering keys(How the data is stored on the disk).
* It includes collections, collections provides flexibility in queries.
* Sets– It gives keeping a unique set of items without the need for read-before-data.
* Lists– In the case of non uniqueness, it takes the maintaining order.
* Maps– It provides a dictionary – like objects with keys and value.

first think about queries, then about data model

#### CQL
It is a client API. It pushes all of the implementation details to the server in the form of a CQL parser.

* CQL 1 was a very basic implementation, it did not support the concept of compound keys.
* CQL 2 supported the concept of compound key which usually referred as wide- row column family.
* CQL 3 has come up with more advancements in compound keys.
* Static Tables--  Irrespective of the logic, it stores the data in each row.
* Dynamic tables– All the logical data will be stored a wide row with the concept of compound key. 

#### Creating Tables

Creating tables:
	
	:::text
        CREATE TABLE users(
		email varchar PRIMARY KEY
		phone varchar,
		birthday timestamp,
		active boolean);

	DROP TABLE users;


#### Replication Factor

It is the process of storing the data into multiple copies
There is no master and slave copy of data, all are having equal priority.
This is for reliability and fault tolerance.
RF should not exceed the number of nodes in cluster, if exceeds writes will be rejected.
The two models in this are 

1. SimpleStrategy  -- With single data center cluster
2. Network Topology Strategy – Across multiple data centers

Replica counts are 1. Two replicas per data center and 2. Three replicas per data center.

#### Snitches

It is a protocol that helps map Ips to racks  and data centers.
It will not work when there is a write operation.
It determines where the data is read from the cluster.

Snitches are  

1. Simple
2. Dynamic
3. Rack Inferring
4. EC2
5. EC2Multiregion.

#### Partittioners
It determines the placement of replicas with in a data center.
Byte oriented partitioner was the first available in cassandra
The byte oriented partitioner follows ordered partitioning.
The advantage is we can scan using primary keys
Random partitioners distributes in a random fashion.

There are two types of random partiotiners available.

1. Random
2. Murmur3


#### Nodetool
Nodetool– it provides basic information about an individual node or all nodes in the cluster ring.

We have so many options for this nodetool which gives us various information.
nodetool  version – Gives us the version of cassandra
nodetool info – Gives us the information about a node
nodetool ring– Gives us the information about cluster.
nodetool flush– it purges the data from memory and writes it to the disk.

#### Compaction

Compaction merges multiple SSTables.
By compaction, it creates new index, combines columns, improves the performance by minimizing the disk seeks.
There are two types of compaction.

* Minor –-  Runs automatically.
* Major – Manually triggered through nodetool.

The strategies are 

* sizeTired compaction, 
* Leveled compaction.

#### Backups

Backups are done by snapshots.
If we take a snapshot, definitely we need to run nodetool flush, otherwise commitlog data will not come into the snapshot.
We can take the backup by nodetool command.
By nodetool clearsnapshot, we can remove snapshots from disk.
For achieving point-in-time recovery, we need to choose CommitLogArchiving.

#### Monitoring

The monitoring options for cassandra are 
Logging –- It uses the standard log file method.
The logging levels are 

* TRACE, 
* DEBUG, 
* INFO, 
* WARN,
* ERROR, 
* FATAL

By changing the Log Levels, we achieve the monitoring.

The other models are JMX and Mbeans.
The standard tool for managing the Mbeans is Jconsole.

#### Commit Log
Commit Log is log of all changes to the tables in Cassandra.
An entry is made into Cassandra before writing to Memtable.
A power failure or Server failure will allows the data to be recovered from the Commit log files.

#### Memtables and SSTables
Memtable are memory structures maintained in the menory. Memtables are stored in memory and written to disk when they are full

SSTables are data structures written by Cassandra onto the disk

* Kept on disk
* Immutable once written
* Periodically compacted for performance


#### Write Operations
The following are the steps for a write:

* CommitLog Entry
  -- First place a write is recorded
  -- Crash recovery mechanism
  -- Write not successful until recorded in commit log
  -- Once recorded in commit log, data is written to Memtable

 * Next Memtable Entry
  -- Data structure in memory
  -- Once memtable size reaches a threshold, it is flushed (appended) to   SSTable  
  -- Several may exist at once (1 current, any others waiting to be flushed)
  -- First place read operations look for data

