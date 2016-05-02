title: Big Data with Hadoop
date: 2016-05-02
description: A Hive tutorial
tags: hive, sql, table, python, regexe, serialization, programming, hadoop, bigdata, yarn

#Hive : Databases and Tables

Hive is installed in the following location in the VM /home/ubuntu/work/apache-hive-1.0.0/. It is already set in the PATH variable.

###Getting Started

Type hive to launch the hive shell

$ hive
You will see the output as shown below and hive prompt

Logging initialized using configuration in jar:file:/home/ubuntu/work/
  apache-hive-1.0.0/lib/hive-common-1.0.0.jar!/hive-log4j.properties
SLF4J: Class path contains multiple SLF4J bindings.
...
SLF4J: Actual binding is of type [org.slf4j.impl.Log4jLoggerFactory]
hive>
DataBases

###Show Existing Databases

Execute the following command to find existing databases created in hive.

hive> show databases;
OK
default
employee_data
retail_demo
Time taken: 0.394 seconds, Fetched: 4 row(s)
Create a new Database

hive> create database employee_data;
OK
Time taken: 0.213 seconds
If the database already exists it will throw an error

hive> create database employee_data;
FAILED: Execution Error, return code 1 from
  org.apache.hadoop.hive.ql.exec.DDLTask.
  Database employee_data1 already exists
Before creating tables in database make sure you execute the following command

hive> use employee_data;
Database Location in HDFS

All databases are created under /user/hive/warehouse directory.

$ hadoop fs -ls /user/hive/warehouse
15/03/16 03:14:54 WARN util.NativeCodeLoader: Unable to load
      native-hadoop library for your platform...
Found 5 items
drwxr-xr-x   - hduser supergroup 0 2015-02-22 01:31 /user/hive/warehouse/employee_data.db
List Tables in a Database

hive> show tables;
Data

We will be using the following Data

John Doe        100000.0        Mary Smith,Todd Jones
        Federal Taxes-.2,State Taxes .05        Insurance-.1
        A1~Michigan Ave~Chicago~IL~B60600
Create Table

We will create an employees table in database employee_data. Following attributes are being specified:

Fields delimited Tab
Map Keys delimited by -, Federal Taxes-.2
Collection Keys delimited by ,, Federal Taxes-.2,State Taxes .05
Lines terminated by New line \n
hive> CREATE TABLE employees (
  name         STRING,
  salary       FLOAT,
  subordinates ARRAY<STRING>,
  deductions   MAP<STRING, FLOAT>,
  address      STRUCT<street:STRING, city:STRING, state:STRING, zip:INT>
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '\t'
COLLECTION ITEMS TERMINATED BY ','
MAP KEYS TERMINATED BY '-'
LINES TERMINATED BY '\n'
STORED AS TEXTFILE;
You can use IF NOT EXISTS clause for hive to check if a table exists before creating a new one.

hive> CREATE TABLE IF NOT EXISTS employees (
  ...
)

###Load Data

Use LOAD DATA command from hive prompt to load data into a Hive table. Example below shows loading employee data from HDFS into employees table we created above.

Load from HDFS

hive> LOAD DATA INPATH '/emp_data/employee.txt' OVERWRITE INTO TABLE employees;
Load from Local FileSystem

Use the keyword LOCAL keyword.

hive> LOAD DATA LOCAL INPATH '<local_file_path>' OVERWRITE INTO TABLE employees;
External Tables

The EXTERNAL keyword tells Hive this table is external and the LOCATION … clause is required to tell Hive where it’s located. Because it’s external, Hive does not assume it owns the data. Therefore, dropping the table does not delete the data, although the metadata for the table will be deleted.

CREATE  EXTERNAL TABLE employees_ext(
      name         STRING,
      salary       FLOAT,
      subordinates ARRAY<STRING>,
      deductions   MAP<STRING, FLOAT>,
      address      STRUCT<street:STRING, city:STRING, state:STRING, zip:INT>
    )
    ROW FORMAT DELIMITED
    FIELDS TERMINATED BY '\t'
    COLLECTION ITEMS TERMINATED BY ','
    MAP KEYS TERMINATED BY '-'
    LINES TERMINATED BY '\n'
    STORED AS TEXTFILE;


###Aggregate functions

SELECT count(*), avg(salary) FROM employees;
Table Generating Functions

hive> SELECT explode(subordinates) AS sub FROM employees;
Mary Smith
Todd Jones
Bill King
Limit Clause

SELECT upper(name), salary, deductions["Federal Taxes"],
round(salary * (1 - deductions["Federal Taxes"])) FROM employees
LIMIT 2;
Nested Select

FROM (
        SELECT upper(name) as name, salary, deductions["Federal Taxes"] as fed_taxes,
        round(salary * (1 - deductions["Federal Taxes"])) as salary_minus_fed_taxes
        FROM employees
        ) e
SELECT e.name, e.salary_minus_fed_taxes
WHERE e.salary_minus_fed_taxes > 70000;
JOHN DOE    100000.0  0.2   80000



#Hive : Partitioned Tables

In this lab we will learn how to create a load a partitioned table in hive

Create Table

hive> CREATE TABLE table1(name STRING, age INT, entry_date STRING)
  ROW FORMAT DELIMITED FIELDS TERMINATED BY ',';
Load Data

hive> LOAD DATA LOCAL INPATH '/home/ubuntu/work/big_data_labs/data/entry_date.csv'
      OVERWRITE INTO TABLE table1;
Show all the Data in the table

hive> select * from table1;
OK
John 45      2012-11-11
Tom  18      2012-11-11
Lars 59      2012-11-11
Bob  34      2012-11-12
Taylor       21      2012-11-12
**Execute a query with a Condition **

We will use run a query to return age where entry_date is 2012-11-11

hive> SELECT
        age
      FROM
        table1
      where entry_date = '2012-11-11';
Partitioned Table

Create a Partitioned Table

hive> CREATE TABLE table2(name STRING, age INT) PARTITIONED BY (entry_date STRING)
ROW FORMAT DELIMITED FIELDS TERMINATED BY ',';
Populate Partitioned Table

INSERT OVERWRITE TABLE table2 PARTITION (entry_date='2012-11-11')
     SELECT name, age FROM table1 WHERE entry_date='2012-11-11';

    INSERT OVERWRITE TABLE table2 PARTITION (entry_date='2012-11-12')
  SELECT name, age FROM table1 WHERE entry_date='2012-11-12';
Run the Select Query again

hive> SELECT
         age
       FROM
         table2
       where entry_date = '2012-11-11';

