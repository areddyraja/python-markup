title: OSGI Basic 
date: 2016-05-02
description: osgi, Apache Camel, Integration, Karaf, JBoss container
tags: JBoss, Fuse, ESB, programming,Apache CXF, Apache Karaf, OSGI


###Overview

###Best practices
Start Small - Many times as developers we are thrown into situations where we have to pick up a new technology very quickly.  9/10 the best way to learn something new is to start small and build from there and osgi is no exception.  Start with a small camel project that requires little to no dependencies that moves a file from one folder to another or something similar.  Once you have that up and running on Fuse then you can begin to expand your project.  https://github.com/FuseByExample as some great sample projects to get your started and familiar with osgi. 


####Import and export dependencies and types
Every Import need and Equivalent Export - Imports and exports may be a difficult concept to grasp at first since often as developers we are used to using Maven and letting Maven just figure it all out for us. Ever come across a bizarre issue where maven is just picking the wrong version of a jar for your war?  Thats why using proper imports and exports and dependency resolution is so important in osgi!  For everything you need to import for your bundle there needs to be an export for it somewhere in your container.  This may come from another one of your bundles such as a custom dependency bundle or it may come from a feature installed in Karaf by default.  Note: Imports and exports are defined by packages.  A subpackage will get included, but if you include a sub-package and not a parent it will not get included. ie. com.example.type will include com.example.type.animals, but com.example.type.animals will not include com.example.type

####Camel ports
When using Ports, You cannot have a multiple camel component endpoints on the same port. 
For example, your project has cxrfs, jetty, and restlet endpoints.  
If these are endpoints you created you will need to give them ports.
You can have many endpoints in the same container with the same port as long as they use the same component (i.e. All cxfrs).
There are ways around this to limit the number of ports you have open. 
Essentially you can use 1 bundle as a proxy to the other bundles. Another important point on ports.  
If you are using apache do not use something like `localhost:8081/services' and 'localhost:8082/services'.
Apache will get confused and not know where to send the traffic to if you have something in front of it such as 'myapp/services'.  

####Bundle
What is a bundle? - Bundles are what we use in osgi to package code.  They are the imports and exports explained above.  The lifecycle of a bundle is another important aspect to consider.  When you first install a bundle on Fuse it gets 'Resolved'.  This means that it is able to find all the imports it is asking for and that the manifest understand that is needed.  This does not guarantee it will start up cleanly.  The next phase is 'Started'.  This indicates that any routes in your bundle have started successfully and were able to find any dependencies required, that the route syntax was valid, and that endpoints could be resolved.  After a bundle is started it can be updated to get new code, uninstalled to be removed from the container, or stopped so it doesn't run anymore.  See more about bundles below.

####General
- A bundle is a small module of code. 
- You can think of a bundle as a jar with additional manifest information specifying packages to import and export
- Bundles can contain camel routes, but do not have to
- If you are using Maven to create/define your bundle you will need to specify the import and export packages
- You can make a regular plain jar into a bundle using maven's wrap feature, but this is not recommended if you can avoid it.  Doing this leaves a bit of 'magic' to be done by maven in defining the manifest.
- Bundles should be an independent from one another as possible, without allowing for duplicate code in your bundles.


####Bundles The Lifecycle
1. INSTALLED - The bundle is installed in Karaf, but may not have all of its required dependencies met.
2. RESOLVED -  The bundle is installed and has all needed dependencies resolved. ***NOTE: This means all known dependencies are resolved, you may still hit run time dependency issues.
3. STARTING -  The bundle is starting up and has all dependencies resolved.
4. ACTIVE - The bundle is started and up and running.  Any services can be hit at this point and any routes will be running.  For a bundle with camel routes you may see both "ACTIVE" and "STARTED" listed as statuses for the bundle in different columns indicating that the routes are running.
5. STOPPED - The bundle is stopped, but still installed.  A bundle which is stopped may or may not have all of its required dependencies.
6. UNINSTALLED - The bundle has been uninstalled.  It will no longer show up in the karaf console.


