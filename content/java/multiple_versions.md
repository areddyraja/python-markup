
There are several JDK implementations: OpenJDK, GNU, JDK from Oracle, etc. All these JDKs come with a ‘java‘ executable. Supposing we got several JDKs from different vendors installed, which will be the one executed in our system when the ‘java‘ program runs?


Check what are the Java alternatives configured in my system:

	:::text
	$ alternatives --config java

	+  1        /usr/lib/jvm/jre-1.6.0-openjdk/bin/java
	*  2        /etc/alternatives/java_sdk/bin/java
	3           /usr/lib/jvm/jre-1.5.0-gcj/bin/java
	4           /usr/java/latest/bin/java
	5           /usr/java/jdk1.7.0/bin/java

So, how to add a new alternative? I run the help first:

	:::text
	$ alternatives --help


So, imagine I’m doing a fresh installation, downloaded the latest version of Oracle JDK 1.6 and would like to add it as an alternative. We should run the following command:

	:::text
	$ sudo alternatives --install /usr/bin/java java  /usr/java/jdk1.6.0_25/bin/java 1000



Now if we list the alternatives for ‘java‘.

	:::text
	$ sudo alternatives --config java

	Selection    Command
	-----------------------------------------------
	*+ 1           /usr/java/jdk1.6.0_25/bin/java


When you run this command the prompt asks you which alternative will be the default.

	:::text
	Enter to keep the current selection[+], or type selection number:

The ‘+‘ symbol indicates the manual default, the ‘***‘ indicates the automatic default (the one with the highest number). In this case as there is only one alternative both signs point to the same alternative.

Let’s add OpenJDK as an alternative (imagine I just downloaded and have successfully installed in my system). I should run the following:

	:::text
	$ sudo alternatives --install /usr/bin/java java /usr/lib/jvm/jre-1.6.0-openjdk/bin/java 2000

	:::text
	$ alternatives --config java

There are 2 programs which provide 'java'.

	:::text
	Selection    Command
	-----------------------------------------------
	1           /usr/java/jdk1.6.0_25/bin/java
	*+ 2        /usr/lib/jvm/jre-1.6.0-openjdk/bin/java

Let’s see what happens if we run ‘java‘ now.

	:::text
	$ java -version
	java version "1.6.0_22"
	OpenJDK Runtime Environment (IcedTea6 1.10.3) (fedora-59.1.10.3.fc15-i386)
	OpenJDK Server VM (build 20.0-b11, mixed mode)


Automatically assigning the highest numbered java version

	:::text
	alternatives --auto java"

Remember that ** is actually ** as it’s listed in the list of alternatives. So, if we would like to remove OpenJDK we should type the following:

	:::text
	$ sudo alternatives --remove java /usr/lib/jvm/jre-1.6.0-openjdk/bin/java

Now  Oracle JDK should be the only alternative available:

	:::text
	$ alternatives --config java

There is 1 program that provides 'java'.

	:::text
	Selection    Command
	-----------------------------------------------
	*+ 1           /usr/java/jdk1.6.0_25/bin/java





