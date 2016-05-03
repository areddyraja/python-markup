title: JBoss Fuse
date: 2016-05-02
description: JBoss Fuse tutorial
tags: JBoss, Fuse, ESB, programming,Apache CXF, Apache Karaf, OSGI


##JBoss ESB
ESB is a standards based integration platform that unifies messaging, web services, data transformation and routing. ESB connects and coordinates different applications across the enterprise with transactional integrity.


##Components

####Apache Camel

####Apache CXF

####Apache ActiveMQ

##Containers

####Apache Karaf
Apache Karaf is a lightweight OSGI container for deploying and managing applications. 

####JBoss Enterprise Application Platform
JBoss EAP is JEE container for deploying web applications.


##Development Model



####Starting Fuse
Download Fuse from the following location.

[Download JBoss Fuse](http://www.jboss.org/products/fuse/download/)
[Download JDK 7](http://www.oracle.com/technetwork/java/javase/downloads/jdk7-downloads-1880260.html)
[Download Maven](https://maven.apache.org/download.cgi)

Set the Path for JDK and Maven to be part of the command line path.
In Linux/Mac you can do this
Copy the following lines to home_dir/.bash_profile

PATH=$PATH:~/apache-maven-3.3.9/bin
export PATH

Make sure JAVA_HOME is set the JDK7 home directory.

Run

```
source ~/.bash_profile
```

Start JBoss Fuse

```
bin/fuse
list
```


###Building a simple CXF Web Service


###Building a simple Router Service

