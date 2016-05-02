title: Big Data with Hadoop
date: 2016-05-02
description: Using Pig for Data processing.
tags: pig, hive, hbase, streaming, python, programming, hadoop, bigdata, yarn

#Getting Started

##Starting pig grunt shell

pig executable is already in your path. Executing pig command will start grunt shell as shown below.

$ pig
Run HDFS Commands from grunt

grunt> fs -cat /ppig/NYSE_dividends
Find Average Dividend Paid

We will find the Average Dividend paid for each Stock based on NYSE data in /ppig/NYSE_dividends

Load Data using load command into Schema exchange, symbol, date, dividend.
grunt> dividends = load '/ppig/NYSE_dividends'
       as (exchange, symbol, date, dividend);
Group rows by symbol
grunt> grouped   = group dividends by symbol;
Iterate over grouped and generate line which is group and Average for dividend. Dividend value is obtained using expression dividends.divided. Store this value in a variable avg.
grunt> avg  = foreach grouped generate group, AVG(dividends.dividend);
Store result avg into HDFS using store command
grunt> store avg into 'average_dividend';
Show the results in the terminal
grunt> fs -cat /user/hduser/average_dividend/*
Loading Tuple Data in Pig

Please transfer tuple_data3.txt to HDFS using the following command. Make sure you have my_data folder inside /ppig - use the following command to create one

grunt> fs -mkdir /ppig/my_data` to create one
grunt> fs -put ./tuple_data3.txt /ppig/my_data/tuple_data3.txt
grunt> fs -cat /ppig/my_data/tuple_data3.txt

(3,8,9)
(4,5,6)
(1,4,7)
(3,7,5)
(2,5,8)
(9,5,8)
grunt> A = LOAD '/ppig/my_data/tuple_data3.txt' AS (t1:tuple(t1a:int,t1b:int,t1c:int))
grunt> DUMP A;
((3,8,9))
((4,5,6))
...
grunt> X  = FOREACH A GENERATE t1.t1a,t1.$1;
grunt> dump X;
Assignment

Calculate Average of t1a and t1b from X and store in Y relation and persist in HDFS



##UDF : User Defined Functions

Pig provides extensive support for user defined functions (UDFs) as a way to specify custom processing. Pig UDFs can be implemented in six languages: Java, Jython, Python, JavaScript, Ruby and Groovy.

The most extensive support is provided for Java functions. Java functions are also more efficient because they are implemented in the same language as Pig and because additional interfaces are supported such as the Algebraic Interface and the Accumulator Interface.

Limited support is provided for Jython, Python, JavaScript, Ruby and Groovy functions. These functions are new, still evolving, additions to the system. Currently only the basic interface is supported; load/store functions are not supported. Furthermore, JavaScript, Ruby and Groovy are provided as experimental features because they did not go through the same amount of testing as Java or Jython. At runtime note that Pig will automatically detect the usage of a scripting UDF in the Pig script and will automatically ship the corresponding scripting jar, either Jython, Rhino, JRuby or Groovy-all, to the backend. Python does not require any runtime engine since it invoke python command line and stream data in and out of it.

Pig also provides support for Piggy Bank, a repository for JAVA UDFs. Through Piggy Bank you can access Java UDFs written by other users and contribute Java UDFs that you have written.

Writing Java UDFs

We are going to use following data-set to learn how to use Java UDFs. This is employee data with name, age and rating. Store the following data in a file emp_data.
raj     30      3.9
murli   34      2.0
Load this data into hdfs under the path /pig-data/emp_data.

$ hadoop fs -put emp_data /pig-data
Next we will create a UDF which converts the names into Upper case.
 1
 2
 3
 4
 5
 6
 7
 8
 9
10
11
12
13
14
15
16
17
18
19
20
        package myudfs;
        import java.io.IOException;
        import org.apache.pig.EvalFunc;
        import org.apache.pig.data.Tuple;

        public class UPPER extends EvalFunc<String>
        {
            public String exec(Tuple input) throws IOException {
                if (input == null || input.size() == 0 ||
                    input.get(0) == null)
                    return null;
                    try{
                        String str = (String)input.get(0);
                        return str.toUpperCase();
                    }catch(Exception e)
                        throw new IOException("Caught" +
                            "exception processing input row ", e);
                    }
            }
        }
Line 1 indicates that the function is part of the myudfs package. The UDF class extends the EvalFunc class which is the base class for all eval functions. It is parameterized with the return type of the UDF which is a Java String in this case. We will look into the EvalFunc class in more detail later, but for now all we need to do is to implement the exec function. This function is invoked on every input tuple. The input into the function is a tuple with input parameters in the order they are passed to the function in the Pig script. In our example, it will contain a single string field corresponding to the student name.

The first thing to decide is what to do with invalid data. This depends on the format of the data. If the data is of type bytearray it means that it has not yet been converted to its proper type. In this case, if the format of the data does not match the expected type, a NULL value should be returned. If, on the other hand, the input data is of another type, this means that the conversion has already happened and the data should be in the correct format. This is the case with our example and that’s why it throws an error (line 15.)

Also, note that lines 9-10 check if the input data is null or empty and if so returns null.

You can copy the code written above from the source repo as listed below. Create a new directory pig-udf under /home/ubuntu/work.

$ mkdir pig-udf
$ cd pig-udf
$ git clone https://github.com/rajdeepd/pig-udf
This will copy the repo and build file for maven to your directory

Compile and create a Jar file

$ mvn package
A jar file myudfs-1.0-SNAPSHOT.jar will get created under target directory

Start the grunt shell and register this jar file

grunt> register /home/ubuntu/work/mortar-pig-java-template/target/myudfs.jar
Load the emp_data from HDFS into relation A.

grunt> A = LOAD '/pig-data/emp_data' AS (name: chararray, age: int, gpa: float);
Call UDF function to convert name into Upper case

grunt> B = FOREACH A GENERATE myudfs.UPPER(name)
On dumping B relation notice that the name has been converted into upper case

grunt> dump B (RAJ) (MURLI)

To summarize we can use customer UDFs to do arbitrary manipulations on data being loaded into Pig.

