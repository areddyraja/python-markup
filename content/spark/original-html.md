 <!-- Page Content -->
<div class="container" id ="doclayout" style="margin-top:30px;">
    <div class="row">

        <div class="col-md-2">
            <aside class="sidebar">

                <ul class="nav">
                    <li class="heading">Apache Spark</li>
                    <li><a is-active-nav href="#introSpark">Introduction</a></li>
                    <li><a is-active-nav href="#getstarted">Getting Started</a></li>
                    <li><a is-active-nav href="#eco-system">Spark Eco System</a></li>

                </ul>

                <ul class="nav">
                    <li class="heading">Getting Started</li>
                    <li><a is-active-nav href="#sparkinstall">Installation</a></li>
                    <li><a is-active-nav href="#sparkexample">Eclipse Setup</a></li>
                </ul>


                <ul class="nav">
                    <li class="heading">Spark Examples</li>
                    <li><a href="#collections-examples">Collections</a></li>
                    <li><a href="#reduce-examples">Reduce</a></li>
                    <li><a href="#group-examples">groupBy</a></li>
                    <li><a href="#writing_to_file">Writing to a File</a></li>
                </ul>

                <ul class="nav">
                    <li class="heading">Spark With Cassandra Examples</li>
                    <li><a href="#gettting_started-cassandra">Start with Cassandra</a></li>
                    <li><a href="#reduce-examples">Reduce</a></li>
                    <li><a href="#group-examples">groupBy</a></li>
                    <li><a href="#writing_to_file">Writing to a File</a></li>
                </ul>


            </aside>
        </div>


        <div class="content">
            <div class="col-md-7" style="margin-top:-18px;">

            <div id="introSpark" style="display:block;margin-top:-50px;"><br><br>
                <h2>Introduction</h2>
                <p>
                Apache Spark is the opensource distributed computing framework, more focussed on iterative computing. It relies on the computation graph for reliability and uses in-memory computing. It is a general purpose cluster computing Platform. Spark is built and developed at Berkeley labs. It is moved to Apache and is written in scala and has the APIs in scala, python and Java. Python spark is getting more popular than Spark Scala.

                </p>

<p>
                Apache Spark is multiple times faster than its predecessor Hadoop due to its design to use memory.
                Hadoop primarily provides MapReduce paradigm, where Apache Spark offers MapReduce and a rich set of API for computing.
</p>
<p>
                pache Spark can be deployed on a Stand alone or on Hadoop or on Mesos.
                Apache spark by default uses File System store. It works HDFS, Apache Cassandra, S3 and may be other storage systems.
                </p>

                <p>
                Apache Spark relies heavily on the concept of RDD. RDD stands for Resilient Distributed Dataset. It provides a handle to individual data partitions which are the result of some computation.
                It provides the basic abstraction for Data representation for Data processing


                RDD provides a collection interface, which gives power to manipulate data, like counts, max, min, group by etc.
                RDD can be cached to provide boost to performance.


                RDD does not restrict to MapReduce paradigm. A simple word count example is shown below:

                <p>
                    SparkContext is available as part of the shell.
                    SparkContext can create a RDD from local files, external data sources like HDFS, database table like JDBC etc.
                    SparkConntext has lot of methods and most used one is the one to create an RDD. RDD is sparks abstraction for collection data distributed over the cluser.
                    RDD is lazily evaluated and immutable.
                </p>

                </p>
                  <div class="codebox">
                    <pre>
val input = sparkContext.textFile("path/to/input/file")
val words = input.flatMap(line => line.split(" "))
val wordsMappedToOne = words.map(word => (word, 1))
val wordOccrCount = wordsMappedToOne.reduceByKey((a, b) => a + b)
wordOccrCount.saveAsTextFile("path/to/output/file")
                    </pre>
                </div>

                <p>
                RDD provides transformations and operations. Transformantions gives a new RDD and operations triggers the actual calculations.
            </p>

            </div>


            <div id="getstarted" style="display:block;margin-top: -50px;"><br><br>
                <h2>Getting Started</h2>
                The tutorial uses  Apache Spark 1.4.1
                The following are the requisites.
                <li>
                    Ubuntu 12 or 14
                </li>
                <li>
                    Apache Spark Installation
                </li>
                <li>
                   Open JDK 1.7
                </li>
                <li>
                    Scala 2.11.7
                </li>
                 <li>
                    Python 2.7.3 for PySpark
                </li>

                A quick example

                <div class="codebox">
                    <pre>
scala> val data = Array(1, 2, 3, 4, 5)
data: Array[Int] = Array(1, 2, 3, 4, 5)
scala> val rddData = sc.parallelize(data)
rddData: org.apache.spark.rdd.RDD[Int] = ParallelCollectionRDD[1] at parallelize at <console>:23
                    </pre>
                </div>
            </div>


            <div id="eco-system" style="display:block;margin-top:-40px;"><br><br>
                <h2>Spark Eco System</h2>
                Spark Eco System has several libraries that provides additional capabilities. Some of the libraries are
                <li>
                    Spark Streaming: used for near real time processing of data. It uses stream of RDD's for processing the data
                </li>
                  <li>
                    Spark SQL: Provides capability to expose datasets over SQL queries
                </li>
                  <li>
                    Spark ML Lib: a scalable Machine Learning Library with commpin machine learning alogorithms such as regression, classification, clustering, collaborative filtering etc.
                </li>
                   <li>
                    Spark GraphX: API for grpahs and parallel computation. 
                </li>
            </div>



                <h2>Development Environment with Eclipse</h2>
                <div class="codebox">
                    <pre>
sbt eclipse
                    </pre>
                </div>

            </div>


  <div id="collections-examples" style="display:block;margin-top:-40px;"><br><br>
                <h3>Collections</h3>
                <p>
                RDD(Resilient Distributed Dataset) is the key Class in the Apache Spark framework.
                RDD when partitioned will be a collections of individual partitions, and can be on separate nodes on a cluster.
               </p>
                <p>
                With RDD handle, one can perform computations and transformations on all partitions within the data
                Whenever a part of the RDD is lost, Spark can recover these RDD's using lineage information. The lineage inforamtion is stored in DAG(Directed acyclic graph) and referes to sequence of transformations resulting in the current/lost RDD. RDD does not impose restirctions on kind of data that can be stored and the API's can handle arbitary data types. 
            </p>
            <p>Most often Spark worked with key value pairs and hence Spark RDD is extended to supported additional functions using PairRDDFunctions, which expllicitly work on paired RDD functions.
            </p>

                <div class="codebox">
                     <p>Invoked Spark Shell
            </p>
                    <pre>
cd SPARK_HOME (go to the installation directory of spark)
bin/spark-shell
                    </pre>
                </div>
            </div>

              <h4>Map</h4>
              <div>
             <p>Map applies transformation function on each of the items in the RDD. The return value is also an RDD
            </p>
              </div>
               <div class="codebox">
        
                    <pre>
#example 1
val fruits = sc.parallelize(List("orange", "apple", "kiwi", "kiwi", "rabbit", "avakado","mango", "grapes", "banana"), 3)
val lengths = fruits.map(_.length)
val fruit_lengths = fruits.zip(lengths)
fruit_lengths.collect
                    </pre>
                </div>

                 <div class="codebox">
        
                    <pre>
#example 2
val names = sc.parallelize(List("Peter","Paul","Mary","John","Harry", 2)
names.map(_.toUppercase)
val fruit_lengths = fruits.zip(lengths)
fruit_lengths.collect
                    </pre>
                </div>



<h4>Folds</h4>
              
              <h4 id="reduce-examples">Reduce</h4>

                <p>Reduces the given input. 
                </p>
                <div class="codebox">
                    <pre>
def reduce(f: (T, T) => T): T
                    </pre>
                </div>
                 <div class="codebox">
                    <pre>
#example 2
val numbers = sc.parallelize(1 to 100, 3)
numbers.reduce( _ + _ )
res0: Int = 5050
                    </pre>
                </div>

                <div class="codebox">
        
                    <pre>
#example 2
val numbers = sc.parallelize(1 to 100, 3)
numbers.reduce( (x,y)=> x + y )
res1: Int = 5050
                    </pre>
                    <p>
                        x is the previous value, and y is the current value. x+y is the cumulative sum of the numbers. The reduce takes a function, which shoud be commutative, other wise, reduce will give different results every time reduce is run on the same data
                    </p>
                </div>

                <h4>Reducing the Tuples using reduceByKey</h4>
                <p>Reduces the given input. 
                </p>
                <div class="codebox">
                    <pre>
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
                    </pre>
                </div>
                 <div class="codebox">
                    <pre>
val views_counts = views.map{case (country, month, program, likes, mins) => ((country,program),(likes, mins) )}.reduceByKey((x,y)=>((x._1+y._1),(x._2+y._2))).collect

views_counts: Array[((String, String), (Int, Int))] = Array(((India,The Robot),(220,2128)), ((US,BreakingBad),(500,5002)), ((US,News),(100,300)), ((India,Friends),(132,518)), ((India,BruceLee),(122,488)), ((US,Friends),(152,1530)), ((India,BreakingBad),(422,1266)), ((US,The Robot),(134,1193))
                    </pre>
                </div>
                    <h5>How it works</h5>
                    <p>The first step is to defnine a map that returns tuples.</p>
                    <p>
                    A key-value tuple is defined where key is also a tuple containing country and program. The value is also a tuple with likes and views.
                    </p>
                <div class="codebox">
                    <pre>
views.map{case (country, month, program, likes, mins) => ((country,program),(likes, mins) )}
                    </pre>
                </div>
                <p>The next step is to reduce values by key. </p>
                <p>The reduce function reduces the two values. x being the previus values and y being the current values. x and y are tuples, each containing (country,program),(likes, mins).
                    Reduce is an associative operation and it works by adding two values first, and then take next set of values and keep adding till all the records are finished.
                    </p>
                <div class="codebox">
                    <pre>
reduceByKey((x,y)=>((x._1+y._1),(x._2+y._2))
                    </pre>
                </div>

              <h4 id="group-examples">groupBy</h4>
              <div class="codebox">
                    <pre>
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
                    </pre>
                </div>

              <h4>SparkSQL and Join</h4>
               <div class="codebox">
                    <pre>
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
                    </pre>
                </div>
              
                <div class="codebox">
                    <pre>
val mappedItems = items.map(item => (item.companyId, item))
val mappedComp = companies.map(comp => (comp.companyId, comp))
mappedItems.join(mappedComp).take(10).foreach(println)

(c1,(Item(1,first,2,c1),Company(c1,company-1,city-1)))
(c1,(Item(2,second,2,c1),Company(c1,company-1,city-1)))
(c2,(Item(3,third,2,c2),Company(c2,company-2,city-2)))

res5: Array[(Int, (String, String))] = Array((10,(jordan,hadoop)), (20,(ricky,spark)), (30,(matt,hive)), (30,(rhonda,hive)))

                    </pre>
                </div>

                <div class="codebox">
                    <pre>

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


                    </pre>
                </div>


                <div class="codebox">
                    <pre>
val emp = sc.parallelize(Seq(("jordan",10), ("ricky",20), ("matt",30), ("mince",35), ("rhonda",30)))
val dept = sc.parallelize(Seq(("hadoop",10), ("spark",20), ("hive",30), ("sqoop",40)))

val shifted_fields_emp = emp.map(t => (t._2, t._1))
val shifted_fields_dept = dept.map(t => (t._2,t._1))

shifted_fields_emp.join(shifted_fields_dept)

                    </pre>
                </div>

               <h4> Joining two csv files with common join key </h4>
               <div class="codebox">
                    <pre>
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

                    </pre>
                </div>



####Joining and filtering data from two data sets 
#method 1

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
#method 2
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

##method3

```
sc.textFile("README.md").
union(sc.textFile("docs/contributing-to-spark.md")).
flatMap(_.split(" ")).
filter(_ == "Spark").
count()
res2: Long = 20
```

####Writing into a File
             
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

####Getting started with Cassandra
Preparing example Cassandra schema
Create a simple keyspace and table in Cassandra. Run the following statements in cqlsh:

<div class="codebox">
                    <pre>
CREATE KEYSPACE test WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1 };
CREATE TABLE test.kv(key text PRIMARY KEY, value int);
Then insert some example data:

INSERT INTO test.kv(key, value) VALUES ('key1', 1);
INSERT INTO test.kv(key, value) VALUES ('key2', 2);
    </pre>
            </div>   

<p>
Now you're ready to write your first Spark program using Cassandra.
Setting up SparkContext

Before creating the SparkContext, set the spark.cassandra.connection.host property to the address of one of the Cassandra nodes:
</p>

            <div class="codebox">
                    <pre>
val conf = new SparkConf(true)
   .set("spark.cassandra.connection.host", "127.0.0.1")
                  </pre>
            </div>   


            </div>       


            <div id="apache6" style="display:block;margin-top:-40px;"><br><br>
                <h2>apache6</h2>
                <hr />

            </div>

            </div>
        </div><!--/content-->


        <div class="col-md-3" id="rightbar">
            <div class="panel panel-default" style="height:1000px;">
                <div class="panel">
                    Ads 
                </div>
            </div>
        </div>

    </div><!--row-->
</div><!--container-->

  <script type="text/javascript">
    $('a[href^="#"]').on('click', function(event) {

    var target = $( $(this).attr('href') );

    if( target.length ) {
        event.preventDefault();
        $('html, body').animate({
            scrollTop: target.offset().top
        }, 1000);
    }

});
</script>


