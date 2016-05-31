title: Big Data with Apache Spark
date: 2016-05-02
description: A tutorial on Apache Spark
tags: spark, programming, hadoop, bigdata, yarn

##Scala: Spark-Sql

###SparkSQL and Join

	:::scala
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

	res5: Array[(Int, (String, String))] = Array((10,(jordan,hadoop)), \
              (20,(ricky,spark)), (30,(matt,hive)), (30,(rhonda,hive)))

        val emp = sc.parallelize(Seq((1,"jordan",10), (2,"ricky",20), 
              (3,"matt",30), (4,"mince",35), (5,"rhonda",30)))

Create dept RDD

	:::scala
	val dept = sc.parallelize(Seq(("hadoop",10), ("spark",20), ("hive",30), ("sqoop",40)))

Establishing that the third field is to be considered as the Key for the emp RDD

	:::scala
	val manipulated_emp = emp.keyBy(t => t._3)

Establishing that the second field need to be considered as the Key for dept RDD

	:::scala
	val manipulated_dept = dept.keyBy(t => t._2)

Inner Join

	:::scala
	val join_data = manipulated_emp.join(manipulated_dept)

	join_data: Array[(Int, ((Int, String, Int), (String, Int)))] = \
               Array((10,((1,jordan,10),(hadoop,10))), (20,((2,ricky,20),(spark,20))), \
		 (30,((3,matt,30),(hive,30))), (30,((5,rhonda,30),(hive,30))))

	val cleaned_joined_data = join_data.map(t => (t._2._1._1, t._2._1._2, t._1, t._2._2._1))


Left Outer Join

	:::scala
	val left_outer_join_data = manipulated_emp.leftOuterJoin(manipulated_dept)

Right Outer Join

	:::scala
	val right_outer_join_data = manipulated_emp.rightOuterJoin(manipulated_dept)
Full Outer Join

	:::scala
	val full_outer_join_data = manipulated_emp.fullOuterJoin(manipulated_dept)

Formatting the Joined Data for better understandable (using map)

	:::scala
	val cleaned_joined_data = join_data.map(t => (t._2._1._1, t._2._1._2, t._1, t._2._2._1))


	val emp = sc.parallelize(Seq(("jordan",10), ("ricky",20), ("matt",30), ("mince",35), ("rhonda",30)))
	val dept = sc.parallelize(Seq(("hadoop",10), ("spark",20), ("hive",30), ("sqoop",40)))

	val shifted_fields_emp = emp.map(t => (t._2, t._1))
	val shifted_fields_dept = dept.map(t => (t._2,t._1))

	shifted_fields_emp.join(shifted_fields_dept)


####Create DataFrame From Json

	:::json
	{"name":"Michael"}
	{"name":"Andy", "age":30}
	{"name":"Justin", "age":19}

	:::python
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

	:::scala
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

	:::scala
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

	:::scala
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

	:::python
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

	:::scala
	~/work/spark/spark-1.3.0-bin-hadoop2.4/bin/spark-submit --class \
	  "sql.StoreParquet" --master local[4] target/scala-2.10/ml-project_2.10-1.0.jar

