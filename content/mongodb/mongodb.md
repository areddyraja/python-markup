title: Mongo DB Tutorials
date: 2016-05-02
description: Mongo DB Tutorials
tags: nosql, bigdata, document database, json, bson, index, mongodb, mongo, mongo index

#### MongoDB Getting Started

Start the Mongo Client

	:::text
	$ mongo
	mongo --help for help and startup options
#### Create a Document

	:::text
	> post = {"title" : "My Blog Post",
	...         "content" : "Here's my blog post.",
	...         "date" : new Date()}
	{
		"title" : "My Blog Post",
		"content" : "Here's my blog post.",
		"date" : ISODate("2015-03-26T03:07:16.440Z")
	}
	> use foobar
	switched to db foobar

#### Insert Data

	:::text
> db.blog.insert(post)
WriteResult({ "nInserted" : 1 })
> db.blog.find()
{ "_id" : ObjectId("5513784b5f861963b603b217"),
  "title" : "My Blog Post",
  "content" : "Here's my blog post.",
  "date" : ISODate("2015-03-26T03:07:16.440Z")
}


#### Access elements in a document

	:::text
	> post.title
	My Blog Post
	Update a Document

	> db.blog.update({title: "My Blog Post"}, post)
	WriteResult({ "nMatched" : 1, "nUpserted" : 0, "nModified" : 1 })
	> db.blog.find()
	{ "_id" : ObjectId("5513784b5f861963b603b217"),
	  "title" : "My Blog Post",
	  "content" : "Here's my blog post.",
	  "date" : ISODate("2015-03-26T03:07:16.440Z"),
	  "comments" : [ ]
	}

#### Remove a Document

	:::text
	> db.blog.remove({title: "My Blog Post"})
	WriteResult({ "nRemoved" : 1 })
	Connect to a remote server

	> conn = new Mongo("some-host:30000")
	db = conn.getDB("myDB")

#### Inserting and Saving Documents

Inserts are the basic method for adding data to MongoDB. To insert a document into a collection, use the collection’s insert method:

	:::text
	> use foo
	switched to db foo
	Single Insert

	> db.foo.insert({"bar" : "baz"})
	Batch Insert

If you have a situation where you are inserting multiple documents into a collection, you can make the insert faster by using batch inserts. Batch inserts allow you to pass an array of documents to the database.

	:::scala
	> db.foo.insert([{"_id" : 0}, {"_id" : 1}, {"_id" : 2}])
	Output of the command is listed below

	BulkWriteResult({
		"writeErrors" : [ ],
		"writeConcernErrors" : [ ],
		"nInserted" : 3,
		"nUpserted" : 0,
		"nMatched" : 0,
		"nModified" : 0,
		"nRemoved" : 0,
		"upserted" : [ ]
		})
	> db.foo.find()
	{ "_id" : 0 }
	{ "_id" : 1 }
	{ "_id" : 2 }

#### Insert Validation
MongoDB does minimal checks on data being inserted: it check’s the document’s basic structure and adds an “_id” field if one does not exist. One of the basic structure checks is size: all documents must be smaller than 16 MB.

	:::text
	> Object.bsonsize(<document>)

#### Removing Documents
The remove function optionally takes a query document as a parameter. When it’s given, only documents that match the criteria will be removed. Suppose, for instance, that we want to remove everyone from the mailing.list collection where the value for “opt-out” is true:

#### Remove a single Document

	:::text
	> db.mailing.list.remove({"opt-out" : true})

Once data has been removed, it is gone forever. There is no way to undo the remove or recover deleted documents.

Statement below removed document with _id= 0, Assuming you have collection foo from the previous section.

	:::text
	> db.foo.remove({"_id":0})
	WriteResult({ "nRemoved" : 1 })
	Execute find() to find the result

	> db.foo.find()
	{ "_id" : 1 }
	{ "_id" : 2 }


#### Removing all documents

This will remove all of the documents in the foo collection. This doesn’t actually remove the collection, and any meta information about it will still exist.

	:::text
	> db.foo.remove({})
	WriteResult({ "nRemoved" : 2 })
	> db.foo.find()


#### Updating Documents

##### Update Complete Document

	:::text
	> joe = {
	...     "name" : "joe",
	...     "friends" : 32,
	...     "enemies" : 2
	... }
	{ "name" : "joe", "friends" : 32, "enemies" : 2 }

	> db.users.insert(joe)
	WriteResult({ "nInserted" : 1 })
	Delete a key and value

	> delete joe.friends
	true

	> db.users.update({"name":"joe"}, joe);
	WriteResult({ "nMatched" : 1, "nUpserted" : 0, "nModified" : 1 })
	Execute find() to check if document got updated.

	> db.users.find()
	{ "_id" : ObjectId("55177c822e018ba3b520e5b4"), "name" : "joe", "enemies" : 2 }
	Updating withObject ID

	    > joe.friends = 0
	    > db.users.update({"_id" : ObjectId("55177c822e018ba3b520e5b4")}, joe)
	    WriteResult({ "nMatched" : 1, "nUpserted" : 0, "nModified" : 1 })

	    > db.users.find()
	    { "_id" : ObjectId("55177c822e018ba3b520e5b4"),
	  "name" : "joe",
	  "enemies" : 2, "friends" : 0
	}


#### Using Modifiers to Update

You can update specific fields in a document using atomic update modifiers. Update modifiers are special keys that can be used to specify complex update operations, such as altering, adding, or removing keys, and even manipulating arrays and embedded documents.

##### Increment : Using $inc

	:::text
	> pageviews = {
		"_id" : ObjectId("4b253b067525f35f94b60a31"),
		"url" : "www.example.com",
		"pageviews" : 52
	}

	> db.analytics.update({"url" : "www.example.com"},
	  {"$inc" : {"pageviews" : 1}})
	WriteResult({ "nMatched" : 1, "nUpserted" : 0, "nModified" : 1 })
	  > db.analytics.find()
	  { "_id" : ObjectId("4b253b067525f35f94b60a31"),
	"url" : "www.example.com", "pageviews" : 53 }
	$set Modifier

$set sets the value of a field. If the field does not yet exist, it will be created. This can be handy for updating schema or adding user-defined keys.

##### Create a user profile as shown below:

	:::text
	> db.users.insert({
	... "_id" : ObjectId("4b253b067525f35f94b60a31"),
	... "name" : "joe",
	... "age" : 30,
	... "sex" : "male",
	... "location" : "Wisconsin"
	... })

If the user wanted to store his favorite book in his profile, he could add it using $set:

	:::text
	> db.users.update({"_id" : ObjectId("4b253b067525f35f94b60a31")},
	... ... {"$set" : {"favorite book" : "War and Peace"}})
	WriteResult({ "nMatched" : 1, "nUpserted" : 0, "nModified" : 1 })
	> db.users.find({"_id" : ObjectId("4b253b067525f35f94b60a31")})
	    { "_id" : ObjectId("4b253b067525f35f94b60a31"),
	... "name" : "joe",
	... "age" : 30,
	... "sex" : "male",
	... "location" : "Wisconsin",
	... "favorite book" : "War and Peace"
	}

#### Querying MongoDB

Perform ad hoc queries on the database using the find or findOne functions and a query
document.

Query for ranges, set inclusion, inequalities, and more by using $-conditionals.
Queries return a database cursor, which lazily returns batches of documents as you need
them.

#### Query Arrays

It behaves like scalars with some additional modifiers

	:::text
	> db.food.insert({"fruit" : ["apple", "banana", "peach"]})
	> db.food.find({"fruit": "apple"}
	{ "_id" : ObjectId("551abd880b4dd0f2cec6659b"), "fruit" : [ "apple", "banana", "peach" ]
	Match more than one fruits

$all If you need to match arrays by more than one element, you can use “$all”. This allows you to match a list of elements.

	:::text
	> db.food.insert({"_id" : 1, "fruit" : ["apple", "banana", "peach"]})
	> db.food.insert({"_id" : 2, "fruit" : ["apple", "kumquat", "orange"]})
	> db.food.insert({"_id" : 3, "fruit" : ["cherry", "banana", "apple"]})
	> db.food.find({fruit : {$all : ["apple", "banana"]}})
		  {"_id" : 1, "fruit" : ["apple", "banana", "peach"]}
		  {"_id" : 3, "fruit" : ["cherry", "banana", "apple"]}

#### Cursors

The database returns results from find using a cursor. The client-side implementations of cursors generally allows user control a great deal about the eventual output of a query. Some of the features are : limit the number of results, skip over some number of results, sort results by any combination of keys in any direction.

	:::text
	> for(i=0; i<100; i++) {
		 db.collection.insert({x : i});
	  }
	> var cursor = db.collection.find();

##### Print the output
> cursor.forEach(function(x) { print(x.name); });




####Indexing
In this Lab you will learn how to create Primary and Compound Indexes on MongoDB documents.

##### Primary Index

	:::text
	> db.users.find({username: "user101"}).explain('executionStats')
	{
		"queryPlanner" : {
			....
		},
		"executionStats" : {
			"executionSuccess" : true,
			"nReturned" : 2,
			"executionTimeMillis" : 117,
			"totalKeysExamined" : 0,
			"totalDocsExamined" : 40692,
			"executionStages" : {
				"stage" : "COLLSCAN",
				"filter" : {
					"username" : {
						"$eq" : "user101"
					}
				},
				"nReturned" : 2,
				"executionTimeMillisEstimate" : 110,
				"works" : 40694,
				"advanced" : 2,
				"needTime" : 40691,
				"needFetch" : 0,
				"saveState" : 317,
				"restoreState" : 317,
				"isEOF" : 1,
				"invalidates" : 0,
				"direction" : "forward",
				"docsExamined" : 40692
			}
		},
		"serverInfo" : {
			"host" : "ubuntu",
			"port" : 27017,
			"version" : "3.0.1",
			"gitVersion" : "534b5a3f9d10f00cd27737fbcd951032248b5952"
		},
		"ok" : 1
	}
	> db.users.ensureIndex({"username" : 1})
	{
		"createdCollectionAutomatically" : false,
		"numIndexesBefore" : 1,
		"numIndexesAfter" : 2,
		"ok" : 1
	}
	> db.users.find({username: "user101"}).explain('executionStats')
	{
		"queryPlanner" : {
			....
		},
		"executionStats" : {
			"executionSuccess" : true,
			"nReturned" : 2,
			"executionTimeMillis" : 15,
			"totalKeysExamined" : 2,
			"totalDocsExamined" : 2,
			"executionStages" : {
				"stage" : "FETCH",
				"nReturned" : 2,
				"executionTimeMillisEstimate" : 0,
				"works" : 3,
				"advanced" : 2,
				"needTime" : 0,
				"needFetch" : 0,
				"saveState" : 0,
				"restoreState" : 0,
				"isEOF" : 1,
				"invalidates" : 0,
				"docsExamined" : 2,
				"alreadyHasObj" : 0,
				"inputStage" : {
					"stage" : "IXSCAN",
					"nReturned" : 2,
					"executionTimeMillisEstimate" : 0,
					"works" : 3,
					"advanced" : 2,
					"needTime" : 0,
					"needFetch" : 0,
					"saveState" : 0,
					"restoreState" : 0,
					"isEOF" : 1,
					"invalidates" : 0,
					"keyPattern" : {
						"username" : 1
					},
					"indexName" : "username_1",
					"isMultiKey" : false,
					"direction" : "forward",
					"indexBounds" : {
						"username" : [
							"[\"user101\", \"user101\"]"
						]
					},
					"keysExamined" : 2,
					"dupsTested" : 0,
					"dupsDropped" : 0,
					"seenInvalidated" : 0,
					"matchTested" : 0
				}
			}
		},
		"serverInfo" : {
			"host" : "ubuntu",
			"port" : 27017,
			"version" : "3.0.1",
			"gitVersion" : "534b5a3f9d10f00cd27737fbcd951032248b5952"
		},
		"ok" : 1
	}

#### Compound Indexes

	:::scala
	> db.users.ensureIndex({"age" : 1, "username" : 1})

#### Aggregation

Aggregation of MongoDB documents while Querying Aggregations operations process data records and return computed results. Aggregation operations group values from multiple documents together, and can perform a variety of operations on the grouped data to return a single result. In sql count(*) and with group by is an equivalent of mongodb aggregation.

Syntax

	:::text
	> db.COLLECTION_NAME.aggregate(AGGREGATE_OPERATION)


#### Group

	:::text
	db.mycol.insert([
	{
	   'title': 'MongoDB Overview',
	   'description': 'MongoDB is no sql database',
	   'by_user': 'tutorials point',
	   'url': 'http://www.tutorialspoint.com',
	   'tags': ['mongodb', 'database', 'NoSQL'],
	   'likes': 100
	},
	{
	   'title': 'NoSQL Overview',
	   'description': 'No sql database is very fast',
	   'by_user': 'tutorials point',
	   'url': 'http://www.tutorialspoint.com',
	   'tags': ['mongodb', 'database', 'NoSQL'],
	   'likes': 10
	},
	{
	   'title': 'Neo4j Overview',
	   'description': 'Neo4j is no sql database',
	   'by_user': 'Neo4j',
	   'url': 'http://www.neo4j.com',
	   'tags': ['neo4j', 'database', 'NoSQL'],
	   'likes': 750
	}])
	> db.mycol.aggregate([{$group : {_id : "$by_user", num_tutorial : {$sum : 1}}}])
	{ "_id" : "Neo4j", "num_tutorial" : 1 }
	{ "_id" : "tutorials point", "num_tutorial" : 2 }


#### Access MongoDB using Python

##### Installing the Driver

	:::text
	$ sudo pip install pymongo

##### Connect to the Server

	:::python
	import pymongo

	    # Connection to Mongo DB
	    try:
		    m_client = pymongo.MongoClient('localhost', 27017)
		    print "Connected successfully!!!"
	    except pymongo.errors.ConnectionFailure, e:
		    print "Could not connect to MongoDB: %s" % e
	    finally:
		    m_client.close()

##### Get List of Databases

	:::python
	import pymongo

	try:
		client = pymongo.MongoClient('localhost', 27017)
		db_list = client.database_names()
		print db_list
	except pymongo.errors.ConnectionFailure, e:
		print "Could not connect to MongoDB: %s" % e
	finally:
		client.close()

###### Insert a Collection

	:::text
	import pymongo

	try:
		client = pymongo.MongoClient('localhost', 27017)
		db = client.test
		users = db.users
		find_one = db.users.find_one()
		print(find_one)
		new_user = {}
		new_user['name'] = 'raj'
		print('new_user %s' % new_user)
		find_user_result = db.users.find(new_user)
		print('find user results: %s' % find_user_result)
		if find_user_result is None:
		    new_user_id = db.users.insert_one(new_user).inserted_id
		    print('new user id %s' % new_user_id)
		else:
		    print('user already exists')
	except pymongo.errors.ConnectionFailure, e:
		print "Could not connect to MongoDB: %s" % e
	finally:
		client.close()


