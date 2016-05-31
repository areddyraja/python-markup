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


####Views and View counts for Australia

	:::scala
	import org.apache.spark.SparkConf
	import org.apache.spark.SparkContext
	import org.apache.spark.sql.cassandra.CassandraSQLContext
	import org.apache.spark.SparkContext.rddToPairRDDFunctions
	import com.datastax.spark.connector.writer.{ RowWriterFactory, TableWriter }
	import com.datastax.spark.connector._
	import com.datastax.spark.connector.rdd.CassandraRDD


	//val conf = new SparkConf(true)
	//new SparkContext(conf)
	//conf = SparkConf().setMaster("spark://172.31.18.36:7077").set("spark.driver.allowMultipleContexts", "true") 


	val rows = sc.cassandraTable("yupptv_analytics_aggregates", "program_stats_by_region_day").where("vendor_id='2' and c_id=-1 and count_type='views' and p_type='live' and day_epoch >= 16725 and day_epoch <= 16756")

	val program_tuples = rows.map(x => (x.getString("country"), x.getString("program_name"), x.getLong("count")))

	val australia = program_tuples.filter{case (country, program_name,count)=> country == "Australia"}
	val australia_only = australia.map { case (country, program_name,count) => (program_name, count)}.reduceByKey((x,y) => ( x + y))

	val csvs = australia_only.sortBy {case (key, value) => -value}.map {case (key, value) => key + "," + value}

	import java.io.File
	import scala.io.Source
	import java.io.PrintWriter

	val writer = new PrintWriter(new File("australia.txt"))
	val data = csvs.collect
	data.foreach(x=>writer.write(x + "\n"))
	writer.close



####Get device statistics for a country by device


The query to be executed

	:::query
	select hour_epoch, min_epoch, session_key, psession_key, 
		device_type, device_id, user_id, city, c_id, p_id 
				from program_sessions_mins 
				where hour_epoch=404323 and 
				min_epoch=24259416 and vendor_id='2' and 
				content_type='vod' and c_id=198 ;

Invoking the Spark shell, copy and paste the following

	:::scala
	import org.joda.time.format.DateTimeFormatter
	import org.joda.time.DateTime
	import org.joda.time.format.DateTimeFormat

	import org.joda.time._
	import org.joda.time.format._

	import org.apache.spark.SparkConf
	import org.apache.spark.SparkContext
	import org.apache.spark.sql.cassandra.CassandraSQLContext
	import org.apache.spark.SparkContext.rddToPairRDDFunctions
	import com.datastax.spark.connector.writer.{ RowWriterFactory, TableWriter }
	import com.datastax.spark.connector._
	import com.datastax.spark.connector.rdd.CassandraRDD
	import java.io.File
	import scala.io.Source
	import java.io.PrintWriter
	import scala.collection.mutable.HashSet
	import org.apache.spark.rdd.RDD
	import org.apache.spark.SparkContext.rddToPairRDDFunctions
	import scala.reflect.{classTag,ClassTag}
	import java.text.SimpleDateFormat
	import java.util.Date



	type S = String

	def getBrowserDetails(agent:S):S = {
	    if(agent.contains("Chrome") )
	      return "Chrome"
	    if(agent.contains("Firefox"))
	      return "Firefox"
	    if(agent.contains("Safari"))
	      return "Safari"
	    if(agent.contains("MSIE"))
	      return "IE"
	    if(agent.contains("OPR") || agent.contains("Opera"))
	      return "Opera"
	    return "Others"
	  }

	def getSpecificDeviceDetails(player:S):S = {
	    if(player.contains("WD"))
	      return "WD"
	    if(player.contains("Sony"))
	      return "Sony"
	    if(player.contains("Opera"))
	      return "Opera App"
	    if(player.contains("Roku"))
	      return "Roku"
	    if(player.contains("Panasonic"))
	      return "Panasonic"
	    if(player.contains("Vizio"))
	      return "Vizio"
	    if(player.contains("LG"))
	      return "LG"
	    if(player.contains("Samsung_2012"))
	      return "Samsung2012"
	    if(player.contains("Samsung_2013"))
	      return "Samsung2013"
	    if(player.contains("Windows"))
	      return "Windows"
	    else 
	      return "Unknown"
	  } 
	def getDeviceDetails(dType:S,clientOs:S,user_agent:S,player_name:S):(S,S) = {
	    val os = clientOs.trim
	      if(dType equals "Browser"){
		return ("Web",getBrowserDetails(user_agent))
	      }
	      if(dType equals "SmartTV"){  
		return ("Devices",getSpecificDeviceDetails(player_name))
	      }
	      if(dType.equals("iPhone") || os.equals("iPhone"))
		return ("Mobile","iPhone")
	      if(dType.equals("iPad") || os.equals("iPad"))
		  return ("Mobile","iPad")
	      if(dType == "iPod" || os == "iPod")
		  return ("Mobile","iPod")
	      if( dType.trim.equals("yupptvmediaplayer"))
		  return ("Device","YuppMediaPlayer")
	      if("firetv".equals(dType))
		  return ("Device","FireTv")
	      if(dType.equals("Android") || os.equals("Android"))
		return ("Mobile","Android")
	      else 
		return ("UnknownDevice","UnknownClient")
	  }

	  

	  

	  object StatsName {
	     case class ColumnSupSet(vendor_id: String, user_id: String, p_id: Long, c_id: Long, program_name: String, session_key: String, platform: String,
				  country_code: String, client: String, timeUnits: Long, p_type: String, count: Long) {
	    }
	  }


	def getAllColunms(r: CassandraRow)(timeDim: String) = {
	    val vendor_id = r.getString("vendor_id")
	    val user_id = r.getString("user_id")
	    val p_id = r.getLong("p_id")
	    val c_id = r.getLong("c_id")
	    val program_name = "Undefined"
	    val session_key = r.getString("session_key")
	    //    if(vendor_id.equals("3") && country_code.equals("India"))
	    //      country_code = r.getString("region")
	    val country_code = "United States"

	    val timeUnits = r.getLong(timeDim)
	    val p_type = r.getString("content_type").toLowerCase()
	    val count = r.getLong("count")
	    val (platform, client) = getDeviceDetails(r.getString("device_type"), r.getString("client_os"), r.getString("user_agent"), r.getString("player_name"))
	    //println("read the row")
	    StatsName.ColumnSupSet(vendor_id, user_id, p_id, c_id, program_name, session_key, platform, country_code, client, timeUnits, p_type, count)
	  }





	val hour_epoch = 404323
	val rows = sc.cassandraTable("yupptv_analytics_collector", "program_sessions_mins").where("hour_epoch = ?", hour_epoch)

	 val x = rows.filter(row=>row.getLong("c_id") == 198)

	 x.collect().foreach(row=>println(row.getString("device_type") +  "," + row.getString("vendor_id") + row.getString("content_type") + "," + row.getString("ip_address") + "," +  row.getString("country") ))

	val all_rows = rows.map(r => getAllColunms(r)("hour_epoch"))


####Get all the stats for Australia

	:::scala
	import org.apache.spark.SparkConf
	import org.apache.spark.SparkContext
	import org.apache.spark.sql.cassandra.CassandraSQLContext
	import org.apache.spark.SparkContext.rddToPairRDDFunctions
	import com.datastax.spark.connector.writer.{ RowWriterFactory, TableWriter }
	import com.datastax.spark.connector._
	import com.datastax.spark.connector.rdd.CassandraRDD


	//val conf = new SparkConf(true)
	//new SparkContext(conf)
	//conf = SparkConf().setMaster("spark://172.31.18.36:7077").set("spark.driver.allowMultipleContexts", "true") 


	val rows = sc.cassandraTable("yupptv_analytics_aggregates", "program_stats_by_region_day").where("vendor_id='2' and c_id=-1 and count_type='views' and p_type='live' and day_epoch >= 16725 and day_epoch <= 16756")

	val rows = sc.cassandraTable("yupptv_analytics_aggregates", "program_stats_by_region_day").where("vendor_id='2' and c_id=-1 and count_type='views' and p_type='live' and day_epoch >= 16725 and day_epoch <= 16756")


	val program_tuples = rows.map(x => (x.getString("country"), x.getString("program_name"), x.getLong("count")))

	val australia = program_tuples.filter{case (country, program_name,count)=> country == "Australia"}
	val australia_only = australia.map { case (country, program_name,count) => (program_name, count)}.reduceByKey((x,y) => ( x + y))

	val csvs = australia_only.sortBy {case (key, value) => -value}.map {case (key, value) => key + "," + value}

	import java.io.File
	import scala.io.Source
	import java.io.PrintWriter

	val writer = new PrintWriter(new File("australia.txt"))

	val data = csvs.collect
	data.foreach(x=>writer.write(x + "\n"))
	writer.close


####Program counts by Country

	:::scala
	bin/spark-shell --master spark://172.31.18.36:7077  --jars /opt/spark-1.4.1-bin-hadoop2.6/lib/spark_cassandra_connector-assembly-1.0.0.jar 


	import org.apache.spark.SparkConf
	import org.apache.spark.SparkContext
	import org.apache.spark.sql.cassandra.CassandraSQLContext
	import org.apache.spark.SparkContext.rddToPairRDDFunctions
	import com.datastax.spark.connector.writer.{ RowWriterFactory, TableWriter }
	import com.datastax.spark.connector._
	import com.datastax.spark.connector.rdd.CassandraRDD


	//val conf = new SparkConf(true)
	//new SparkContext(conf)
	//conf = SparkConf().setMaster("spark://172.31.18.36:7077").set("spark.driver.allowMultipleContexts", "true") 



	val rows = sc.cassandraTable("yupptv_analytics_aggregates", "program_stats_by_region_day").where("vendor_id='2' and c_id=-1 and count_type='views' and p_type='live' and day_epoch >= 16725 and day_epoch <= 16756")

	val rows = sc.cassandraTable("yupptv_analytics_aggregates", "program_stats_by_region_day").where("vendor_id='2' and c_id=-1 and count_type='views' and p_type='live' and day_epoch >= 16725 and day_epoch <= 16756")


	val program_tuples = rows.map(x => (x.getString("country"), x.getString("program_name"), x.getLong("count")))

	val australia = program_tuples.filter{case (country, program_name,count)=> country == "Australia"}
	val australia_only = australia.map { case (country, program_name,count) => (program_name, count)}.reduceByKey((x,y) => ( x + y))

	val csvs = australia_only.sortBy {case (key, value) => -value}.map {case (key, value) => key + "," + value}

	import java.io.File
	import scala.io.Source
	import java.io.PrintWriter

	val writer = new PrintWriter(new File("australia.txt"))

	val data = csvs.collect

	data.foreach(x=>writer.write(x + "\n"))

	writer.close


####Session Verification

Verify the sessions for a particular user

	:::scala
	import org.joda.time.format.DateTimeFormatter
	import org.joda.time.DateTime
	import org.joda.time.format.DateTimeFormat

	import org.joda.time._
	import org.joda.time.format._

	import org.apache.spark.SparkConf
	import org.apache.spark.SparkContext
	import org.apache.spark.sql.cassandra.CassandraSQLContext
	import org.apache.spark.SparkContext.rddToPairRDDFunctions
	import com.datastax.spark.connector.writer.{ RowWriterFactory, TableWriter }
	import com.datastax.spark.connector._
	import com.datastax.spark.connector.rdd.CassandraRDD
	import java.io.File
	import scala.io.Source
	import java.io.PrintWriter
	import scala.collection.mutable.HashSet




	  def loadUserIds = {
	    val userIdHashSet = HashSet[String]()
	    val srcUserIds = Source.fromFile("/opt/sparkjobs/CustomerIDs.txt").getLines()
	    for (line <- srcUserIds.drop(1)) {
	      userIdHashSet += line.trim()
	    }
	    userIdHashSet
	  }
	   val x = loadUserIds
	    x.size


	val day_epoch = 16783
	  val rows = sc.cassandraTable("yupptv_analytics_collector", "program_sessions_days").where("day_epoch = ? and vendor_id = ?", day_epoch, "2")

	//ows.count()
	val country = List("United States", "US","0")
	    val timeFieldName = "day_epoch"



	    val user_rows = rows.filter { r =>   
		  (  country.contains(
		       if (r.getStringOption("country").nonEmpty) 
			   r.getString("country") 
		       else "undefined1233"
		       )  && x.contains(r.getString("user_id"))
		  )          
	    }


	    val count = user_rows.map { r => (r.getString("user_id")) }.distinct().count()



	val uniq_sessions = user_rows.map(y=>(y.getInt("c_id"), y.getInt("count"),y.getInt("p_id"), y.getString("session_key")))



	//for view mins
	val count_rows = uniq_sessions.map({case (cid,count,pid, session_key) => (session_key, count)})
	val crows_views = count_rows.map(x=>x._2).reduce((a,b)=>a+b)



	//for view mins
	val views = count_rows.reduceByKey( _ + _).map(x=>(x._2)).reduce(_+_)

####Users Information

	bin/spark-shell --master spark://172.31.18.36:7077  --total-executor-cores 6 --executor-memory 8G --jars /opt/spark-1.4.1-bin-hadoop2.6/lib/spark_cassandra_connector-assembly-1.0.0.jar,/opt/sparkjobs/populate_stats-assembly-2.0.0.jar



	def isHeader(line: String): Boolean = 
	{ 
	    line.contains("UserId") || line.contains("ChannelName")
	}

	import org.joda.time.format.DateTimeFormatter
	import org.joda.time.DateTime
	import org.joda.time.format.DateTimeFormat

	import org.joda.time._
	import org.joda.time.format._

	import org.apache.spark.SparkConf
	import org.apache.spark.SparkContext
	import org.apache.spark.sql.cassandra.CassandraSQLContext
	import org.apache.spark.SparkContext.rddToPairRDDFunctions
	import com.datastax.spark.connector.writer.{ RowWriterFactory, TableWriter }
	import com.datastax.spark.connector._
	import com.datastax.spark.connector.rdd.CassandraRDD
	import java.io.File
	import scala.io.Source
	import java.io.PrintWriter



	import scala.io._
	val lines=Source.fromFile("india_channels.csv").getLines().filter(x => !isHeader(x))
	val temp = lines.collect(x=> x.split(",") match {
		case Array(s1, s2, s3, s4, s5) => (s1.trim, s2, s3.trim)
	})

	val channel_names = temp.toArray



	val raw_user_subs=Source.fromFile("paid_users.csv").getLines().toList

	def splitLine(line: String) = {
		val splits = line.split(",")
		(splits(0), splits(1),splits(2).split(" ")(0).trim,splits(3).split(" ")(0).trim)
	}


	//DateTimeFormat.forPattern("MM/dd/yy").parseDateTime("09/01/15").getMillis/(3600*1000*24)
	//DateTimeFormat.forPattern("MM/dd/yy").parseDateTime(x._3).getMillis/(3600*1000*24)
	//DateTimeFormat.forPattern("MM/dd/yy").parseDateTime(x._4).getMillis/(3600*1000*24)
	//val user_subs = raw_user_subs.filter(x => !isHeader(x)).map(splitLine(_)).map(x=>(x._1, x._2,     DateTime.parse(x._3, DateTimeFormat.forPattern("MM/DD/YY")).getMillis/(1000*3600*24)        ,    DateTime.parse(x._4, DateTimeFormat.forPattern("MM/DD/YY")).getMillis/(1000*3600*24)
	      ))


	val user_subs = raw_user_subs.filter(x => !isHeader(x)).map(splitLine(_)).map(x=>(x._1, x._2,     DateTimeFormat.forPattern("MM/dd/yyyy").parseDateTime(x._3).getMillis/(3600*1000*24)       ,    DateTimeFormat.forPattern("MM/dd/yyyy").parseDateTime(x._4).getMillis/(3600*1000*24)
	      ))

	val userid_map=user_subs.map(x=>(x._1, x._2)).toMap

	//val jsb = new java.lang.StringBuilder();
	//val day_criteria = jsb.append("(").append(List(16761, 16760, 16759, 16758).mkString(",")).append(")")
	//val days_list=List(16761, 16760, 16759, 16758)

	val current_hour_epoch = new DateTime().getMillis/(3600*24*1000)

	val day_epoch_range=(current_hour_epoch-30) to current_hour_epoch mkString(",")

	val day_criteria=List( "(", day_epoch_range + ")" ).mkString


	//better-one
	val _rows = sc.cassandraTable("yupptv_analytics_collector", "program_sessions_days").where("day_epoch in ? and vendor_id=? and content_type=?", (current_hour_epoch-30) to current_hour_epoch, "3", "live" )

	//val _rows = sc.cassandraTable("yupptv_analytics_collector", "program_sessions_days").where("day_epoch in " + day_criteria + " and vendor_id='3' and content_type='live'")

	val user_rows = _rows.filter(row=>userid_map.exists(_._1 == row.getString("user_id"))).map(y=>(y.getInt("c_id"), y.getInt("count"),y.getInt("p_id"), y.getString("user_id"), y.getString("session_key")))


	//for mins
	val channel_rows = user_rows.map({case (cid,count,pid,userid, session_key) => cid->count}).reduceByKey( _ + _).collect
	val total_count_views = channel_rows.map(x=>(x._2)).reduce(_+_)

	//Join counts with the channel names and their percentages
	val users_channel_mins = for(
		a <- channel_rows;
		b <- channel_names if(a._1 == b._2.toInt) 
	) yield(b,(a._2*100.0/total_count_views),a._2)


	val writer4 = new PrintWriter(new File("user_channel_statistics.csv"))
	users_channel_mins.sortWith(_._2 > _._2).foreach(x=>writer4.write(x._1 + "," + x._2 + "\n"))
	writer4.close


	//for views
	val channel_rows_for_views = user_rows.map({case (cid,count,pid,userid, session_key) => (session_key, cid)->count})
	val crows_views = channel_rows_for_views.reduceByKey(_ + _)
	val views = crows_views.map(x=>(x._1._2,1))
	val final_views= views.reduceByKey(_ + _).collect

	val total_final_views = final_views.map(_._2).reduceLeft(_ + _)

	//Join counts with the channel names and their percentages
	val users_channel_views = for(
		a <- final_views;
		b <- channel_names if(a._1 == b._2.toInt) 
	) yield(b,(a._2*100.0/total_final_views),a._2)


	val writer5 = new PrintWriter(new File("user_channel_statistics_views.csv"))
	users_channel_views.sortWith(_._2 > _._2).foreach(x=>writer5.write(x._1 + "," + x._2 + "\n"))
	writer5.close

	val resultsGrpViews = users_channel_views.map(a=>(a._1._3,a._3))
	val rdd2_views = sc.parallelize(resultsGrpViews)
	val lang_counts_views = rdd2_views.reduceByKey((a,b)=> a+b).collect

	val writer5 = new PrintWriter(new File("user_langs.csv"))
	lang_counts_views.sortWith(_._2 > _._2).foreach(x=>writer5.write(x._1 + "," + x._2 + "\n"))
	writer5.close



	// A single paid user has paid for some paid channel. We want to know which paid channel he is watching regularly. Whcih free channel he is watching regularly - Watching means views/mins that he is watching for the channel.


	val user_rows_region = _rows.filter(row=>userid_map.exists(_._1 == row.getString("user_id"))).map(y=>(y.getInt("c_id"), y.getInt("count"),y.getInt("p_id"), y.getString("user_id"), y.getString("session_key"), y.getString("region")))

	val region_rows_for_views = user_rows_region.map({case (cid,count,pid,userid, session_key, region) => (session_key, region)->count})

	val r_views = region_rows_for_views.reduceByKey(_ + _)
	val rviews = r_views.map(x=>(x._1._2,1))
	val r_final_views= rviews.reduceByKey(_ + _).collect

	val total_final_views = final_views.map(_._2).reduceLeft(_ + _)

	val writer5 = new PrintWriter(new File("region_views.csv"))
	r_final_views.sortWith(_._2 > _._2).foreach(x=>writer5.write(x._1 + "," + x._2 + "\n"))
	writer5.close


	//By languages in terms of percentage


	//for unique users across regions
	val user_rows_region = _rows.filter(row=>userid_map.exists(_._1 == row.getString("user_id"))).map(y=>(y.getInt("c_id"), y.getInt("count"),y.getInt("p_id"), y.getString("user_id"), y.getString("session_key"), y.getString("region")))

	val region_rows_for_views = user_rows_region.map({case (cid,count,pid,userid, session_key, region) => (region, userid)->count})



	val r_views = region_rows_for_views.reduceByKey(_ + _)
	val rviews = r_views.map(x=>(x._1._1,1))
	val r_final_views= rviews.reduceByKey(_ + _).collect
	val total_users = r_final_views.map(_._2).reduceLeft(_ + _)



	val writer5 = new PrintWriter(new File("users_by_region.csv"))
	r_final_views.sortWith(_._2 > _._2).foreach(x=>writer5.write(x._1 + "," + x._2 + "\n"))
	writer5.close


####Get Device statistics for a given Date range

	:::scala
	bin/spark-shell --master spark://172.31.18.36:7077  --total-executor-cores 6 --executor-memory 8G  --jars /opt/spark-1.4.1-bin-hadoop2.6/lib/spark_cassandra_connector-assembly-1.0.0.jar,/opt/sparkjobs/populate_stats-assembly-2.0.0.jar


	import org.joda.time.format.DateTimeFormatter
	import org.joda.time.DateTime
	import org.joda.time.format.DateTimeFormat

	import org.joda.time._
	import org.joda.time.format._

	import org.apache.spark.SparkConf
	import org.apache.spark.SparkContext
	import org.apache.spark.sql.cassandra.CassandraSQLContext
	import org.apache.spark.SparkContext.rddToPairRDDFunctions
	import com.datastax.spark.connector.writer.{ RowWriterFactory, TableWriter }
	import com.datastax.spark.connector._
	import com.datastax.spark.connector.rdd.CassandraRDD
	import java.io.File
	import scala.io.Source
	import java.io.PrintWriter
	import scala.collection.mutable.HashSet
	import org.apache.spark.rdd.RDD
	import org.apache.spark.SparkContext.rddToPairRDDFunctions
	import scala.reflect.{classTag,ClassTag}
	import java.text.SimpleDateFormat
	import java.util.Date


	//val day_epoch = 16840L 

	  def loadUserIds = {
	    val userIdHashSet = HashSet[String]()
	    val srcUserIds = Source.fromFile("/opt/sparkjobs/CustomerIDs.txt").getLines()
	    for (line <- srcUserIds.drop(1)) {
	      userIdHashSet += line.trim()
	    }
	    userIdHashSet
	  }
	   val x = loadUserIds
	    x.size



	type S = String

	def getBrowserDetails(agent:S):S = {
	    if(agent.contains("Chrome") )
	      return "Chrome"
	    if(agent.contains("Firefox"))
	      return "Firefox"
	    if(agent.contains("Safari"))
	      return "Safari"
	    if(agent.contains("MSIE"))
	      return "IE"
	    if(agent.contains("OPR") || agent.contains("Opera"))
	      return "Opera"
	    return "Others"
	  }

	def getSpecificDeviceDetails(player:S):S = {
	    if(player.contains("WD"))
	      return "WD"
	    if(player.contains("Sony"))
	      return "Sony"
	    if(player.contains("Opera"))
	      return "Opera App"
	    if(player.contains("Roku"))
	      return "Roku"
	    if(player.contains("Panasonic"))
	      return "Panasonic"
	    if(player.contains("Vizio"))
	      return "Vizio"
	    if(player.contains("LG"))
	      return "LG"
	    if(player.contains("Samsung_2012"))
	      return "Samsung2012"
	    if(player.contains("Samsung_2013"))
	      return "Samsung2013"
	    if(player.contains("Windows"))
	      return "Windows"
	    else 
	      return "Unknown"
	  } 
	def getDeviceDetails(dType:S,clientOs:S,user_agent:S,player_name:S):(S,S) = {
	    val os = clientOs.trim
	      if(dType equals "Browser"){
		return ("Web",getBrowserDetails(user_agent))
	      }
	      if(dType equals "SmartTV"){  
		return ("Devices",getSpecificDeviceDetails(player_name))
	      }
	      if(dType.equals("iPhone") || os.equals("iPhone"))
		return ("Mobile","iPhone")
	      if(dType.equals("iPad") || os.equals("iPad"))
		  return ("Mobile","iPad")
	      if(dType == "iPod" || os == "iPod")
		  return ("Mobile","iPod")
	      if( dType.trim.equals("yupptvmediaplayer"))
		  return ("Device","YuppMediaPlayer")
	      if("firetv".equals(dType))
		  return ("Device","FireTv")
	      if(dType.equals("Android") || os.equals("Android"))
		return ("Mobile","Android")
	      else 
		return ("UnknownDevice","UnknownClient")
	  }

	  object StatsName {
	     case class ColumnSupSet(vendor_id: String, user_id: String, p_id: Long, c_id: Long, program_name: String, session_key: String, platform: String,
				  country_code: String, client: String, timeUnits: Long, p_type: String, count: Long) {
	    }
	  }


	def getAllColunms(r: CassandraRow)(timeDim: String) = {
	    val vendor_id = r.getString("vendor_id")
	    val user_id = r.getString("user_id")
	    val p_id = r.getLong("p_id")
	    val c_id = r.getLong("c_id")
	    val program_name = "Undefined"
	    val session_key = r.getString("session_key")
	    //    if(vendor_id.equals("3") && country_code.equals("India"))
	    //      country_code = r.getString("region")
	    val country_code = "United States"

	    val timeUnits = r.getLong(timeDim)
	    val p_type = r.getString("content_type").toLowerCase()
	    val count = r.getLong("count")
	    val (platform, client) = getDeviceDetails(r.getString("device_type"), r.getString("client_os"), r.getString("user_agent"), r.getString("player_name"))
	    //println("read the row")
	    StatsName.ColumnSupSet(vendor_id, user_id, p_id, c_id, program_name, session_key, platform, country_code, client, timeUnits, p_type, count)
	  }

	val day_epoch_range = 16815L to 16821L 

	day_epoch_range.foreach { day_epoch =>  

	 
	val rows = sc.cassandraTable("yupptv_analytics_collector", "program_sessions_days").where("day_epoch = ? and vendor_id = ?", day_epoch, "2")

	//ows.count()
	val country = List("United States", "US","0")

	       val user_rows = rows.filter { r =>   
		  (  country.contains(
		       if (r.getStringOption("country").nonEmpty) 
			   r.getString("country") 
		       else "undefined1233"
		       )
		  )    
	    }

	user_rows.cache()
	user_rows.count()

	//filter records by day
	val timeFieldName = "day_epoch"

	val all_rows = user_rows.map(r => getAllColunms(r)(timeFieldName))
	//rdd of ColumnSupSet

	val subscribed_users = all_rows.filter(r=>x.contains(r.user_id))

	//viewmins
	val filter1= subscribed_users.map(row => ((row.timeUnits, row.platform, row.client, row.p_type),row.count)  ).reduceByKey(_ + _ )
	val total_viewmins = filter1.collect()

	//views
	val views = subscribed_users.map(row => ((row.timeUnits, row.platform, row.client, row.p_type, row.session_key),1L)  ).reduceByKey( _ + _ ).map(p=>((p._1._1, p._1._2, p._1._3, p._1._4),p._2)).reduceByKey( _+ _)
	val total_views = views.collect()

	//user list
	val deviceList = views.map(row=> row._1._3).collect
	val clientsLive = for(p <- deviceList) yield {    
	    (p, subscribed_users.filter(row=> row.client.equals(p) && row.p_type.equals("live")).map(r=>r.user_id).distinct().count())
	} 

	//user list
	val clientsVOD = for(p <- deviceList) yield {    
	    (p, subscribed_users.filter(row=> row.client.equals(p) && row.p_type.equals("vod")).map(r=>r.user_id).distinct().count())
	} 

	val report = for (q <- deviceList ) yield {
	   //live
	   val minsLive = total_viewmins.filter(x=>q.equals(x._1._3) && x._1._4.equals("live"))
	   val minsLivecheck = if(minsLive.nonEmpty)  minsLive(0)._2 else  0L

	   val viewsLive = total_views.filter(x=>q.equals(x._1._3) && x._1._4.equals("live"))
	   val viewLivecheck = if(viewsLive.nonEmpty)  viewsLive(0)._2 else  0L

	   //vod
	   val minsVOD = total_viewmins.filter(x=>q.equals(x._1._3) &&  x._1._4.equals("vod"))   
	   val vodcheck = if(minsVOD.nonEmpty) 
		   minsVOD(0)._2
		    else
		   0L

	   val viewsVOD = total_views.filter(x=>q.equals(x._1._3) && x._1._4.equals("vod") )
	   val viewVODcheck = if(viewsVOD.nonEmpty)  viewsVOD(0)._2 else  0L

	  val userlivecount = clientsLive.filter(x=>q.equals(x._1))
	  val userLivecheck = if(userlivecount.nonEmpty)  userlivecount(0)._2 else  0L

	  val uservodcount = clientsVOD.filter(x=>q.equals(x._1))
	   val userVODcheck = if(uservodcount.nonEmpty)  uservodcount(0)._2 else  0L

	   (day_epoch, q, minsLivecheck,viewLivecheck, userLivecheck, vodcheck, viewVODcheck, userVODcheck, userLivecheck+userVODcheck)
	}

	import java.io.File
	import scala.io.Source
	import java.io.PrintWriter
	import java.io.FileWriter

	val writer = new PrintWriter(new FileWriter("/home/yuppindia/report.csv", true))
	val date = new SimpleDateFormat("dd-MMM-yyyy").format(new Date(day_epoch * 24 * 60 * 60 * 1000))

	report.foreach(x=>writer.write(date + "," +  x._2 + "," + x._3 + "," + x._4 + "," +  x._5 + "," + x._6 + "," + x._7 + "," + x._8 +  "," + x._9 +  "\n"))
	writer.close

	}
