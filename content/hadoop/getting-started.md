title: Getting started with Hadoop
date: 2016-05-02
description: A tutorial explaining how to set up a hadoop 
tags: programming, hadoop, bigdata, yarn

#Getting Started

###Logging into the VM

VM username : ubuntu Password : ubuntu

Hadoop installation dir : /home/ubuntu/work/hadoop-2.6.0

Login as hduser, password : hduser

$ su hduser
Starting hadoop

To start hadoop daemon execute the shell scripts start-dfs.sh and start-yarn.sh. These scripts will start the following daemons

* NameNode
* DataNode
* ResourceManager
* JobManager
* SecondaryNameNode daemons.

```
$ /home/ubuntu/work/hadoop-2.6.0/sbin/start-dfs.sh
$ /home/ubuntu/work/hadoop-2.6.0/sbin/start-yarn.sh
```

You will need to start the Job History Server for Pig to run.

```
$ mr-jobhistory-daemon.sh start historyserver
```
###HDFS Commands

####List Files in HDFS
```
hadoop fs -ls /
```
####Upload a File to HDFS
```
hadoop fs -put isb_sectiona.txt /isb_sectiona.txt
```
####List contents of a file in HDFS.
Note Both the commands below will work
```
hadoop fs -cat /isb_sectiona.txt
hadoop fs -cat hdfs://localhost:9000/isb_sectiona.txt
```
####Create a Directory in HDFS. 
```
hadoop fs -mkdir <path_to_directory>
```
<path_to_directory> is the Absolute path of the Directory for example /mydir.
####Delete a Directory from HDFS.
```
hadoop fs -rmr <path_to_directory>
```

####Hadoop ClassPath

Hadoop Classpath has to be set for it to be able to find the class file being executed. In this case we are giving fullpath of hadoop-examples.jar

```
export HADOOP_CLASSPATH=/home/ubuntu/work/hadoop-book/hadoop-examples.jar
```

To Compile/ Re-Compile the Hadoop Examples Execute the following command.

```
$ mvn compile
$ mvn -DskipTests install
```
Note Make sure you are in the folder /home/ubuntu/work/hadoop-book/
###HDFS APIs

####Show contents of a file in HDFS by using URL

HDFS APIs allow you to access the Hadoop FileSystem programmatically for reading / writing the data. Execute the following Java Program URLCat to read file from HDFS and display on the terminal. wikipedia.txt is sample file which needs to be replaced by any text file existing on your HDFS.

```
public class URLCat {
    static {
                    URL.setURLStreamHandlerFactory(
                        new FsUrlStreamHandlerFactory());
            }

            public static void main(String[] args) throws Exception {
            InputStream in = null;
            try {
                      in = new URL(args[0]).openStream();
                      IOUtils.copyBytes(in, System.out, 4096, false);
            } finally {
                IOUtils.closeStream(in);
            }
    }
```

####Show contents of a file by using org.apache.hadoop.fs.FileSystem
```
hadoop URLCat hdfs://127.0.0.1:9000/hadoop-book/wikipedia.txt
```

```
public class FileSystemCat {
      public static void main(String[] args) throws Exception {
            String uri = args[0];
            Configuration conf = new Configuration();
            FileSystem fs = FileSystem.get(URI.create(uri), conf);
            InputStream in = null;
            try {
              in = fs.open(new Path(uri));
              IOUtils.copyBytes(in, System.out, 4096, false);
            } finally {
              IOUtils.closeStream(in);
            }
      }
    }
```

```
hadoop FileSystemCat hdfs://127.0.0.1:9000/hadoop-book/wikipedia.txt
```
####Copy a File to HDFS

```
public class FileCopyWithProgress {
  public static void main(String[] args) throws Exception {
        String localSrc = args[0];
        String dst = args[1];

        InputStream in = new BufferedInputStream(
    new FileInputStream(localSrc));

        Configuration conf = new Configuration();
        FileSystem fs = FileSystem.get(URI.create(dst), conf);
        OutputStream out = fs.create(new Path(dst),
    new Progressable() {
          public void progress() {
            System.out.print(".");
          }
        });

        IOUtils.copyBytes(in, out, 4096, true);
  }
}
```

```
hadoop FileCopyWithProgress test.txt hdfs://127.0.0.1:9000/hadoop-book/test.txt
```

####Conclusion
The tutorial provided basic concetps of Hadoop and HDFS.

