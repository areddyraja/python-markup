title: Apache Camel Services
date: 2016-05-02
description: Apache Camel, Integration, Karaf, JBoss container
tags: JBoss, Fuse, ESB, programming,Apache CXF, Apache Karaf, OSGI


###Overview
Camel is used for routing. Essentially we set up an endpoint either from a rest endpoint, a timer, a queue, or an S3 location (for our project specifically, there are MANY other types of endpoints) and from there we can route our message appropriately.  We can do things based on the message contents, based on headers, and many other variables. 

We use java DSL when defining our camel routes, but you can use xml to define them. 

Camel has many components http://camel.apache.org/components.html which can be used to help integrate with other systems. 

Camel allows for easy exception handling based on specific exceptions as well as had a try/catch/finally pattern.  
This pattern is even more extensive than the java one allowing for multiple separate catches based on the exception. 




