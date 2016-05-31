title: Cassandra Tutorials
date: 2016-05-02
description: A tutorial on Docker
tags: docker, kubernets, spark, programming, hadoop, bigdata, yarn

####Apache Cassandra installation  
Recommendations for production environments; adjust them accordingly for your implementation. This installation is applicable for 14.04.5 Ubuntu  os.

###Steps

##### Disable zone_reclaim_mode on NUMA systems
The Linux kernel can be inconsistent in enabling/disabling zone_reclaim_mode. This can result in odd performance problems.
To ensure that zone_reclaim_mode is disabled:

	:::text
	#echo 0 > /proc/sys/vm/zone_reclaim_mode
For more information, see Peculiar Linux kernel performance problem on NUMA systems.

#####User resource limits
You can view the current limits using the ulimit -a command. Although limits can also be temporarily set using this command, DataStax recommends making the changes permanent:  
Packaged installs: Ensure that the following settings are included in the /etc/security/limits.d/cassandra.conf file:

	:::text
	cassandra - memlock unlimited
	cassandra - nofile 100000
	cassandra - nproc 32768
	cassandra - as unlimited

Tarball installs: Ensure that the following settings are included in the /etc/security/limits.conf file:

	:::text
* - memlock unlimited
* - nofile 100000
* - nproc 32768
* - as unlimited

If you run Cassandra as root, some Linux distributions such as Ubuntu, require setting the limits for root explicitly instead of using *:
Edit /etc/security/limits.conf
root - memlock unlimited
root - nofile 100000
root - nproc 32768
root - as unlimited

##### Add the following line to /etc/sysctl.conf :

	:::test
	vm.max_map_count = 131072

To make the changes take effect, reboot the server or run the following command:
$sudo sysctl -p

 Install Java 1.7 

##### Update your system with packages
$sudo apt-get update;apt-get upgrade -y;apt-get dist-upgrade –y

##### Download java from below url
http://www.oracle.com/technetwork/java/javase/downloads/jdk7-downloads-1880260.html

##### Untar the tar ball and install at /usr/lib/jvm/ directory:

	:::text
	#mkdir -p /usr/lib/jvm/
	#tar xvf jdk-7u71-linux-x64 .gz  -C  /usr/lib/jvm

##### To create a softlink

	:::text
	#cd /usr/lib/jvm
	#ln -s  jdk1.7.0_71  java-1.7.0-sun-amd64

##### Verify new java settings

	:::text
	Java –version

       Ref : http://www.cyberciti.biz/faq/howto-installing-oracle-java7-on-ubuntu-linux/


##### Install Cassandra

Download Cassandra 2.1.1
wget  http://apache.mesi.com.ar/cassandra/2.1.1/apache-cassandra-2.1.1-bin.tar.gz  

Extract file

	:::text
	#tar -xzf apache-cassandra-2.1.1-bin.tar.gz

##### Relocate Cassandra Directory

	:::text
	#mkdir  /cassandra-server
	#mount  /dev/sdb1 /Cassandra-server
	#cd apache-cassandra-2.1.1 
	# mv * /cassandra-server/
	# mkdir /cassandra-server/{commitlog,log,,saved_caches}
	#mkdir  /cassandra-data/
	#mount /dev/sdc1 /Cassandra-data/
	#mkdir  /cassandra-data/data

##### Edit Configuration File

	:::text
	#cd  /cassandra-server
	#vi conf/cassandra.yaml
	Modify the Following Lines:
	data_file_directories:
	– /Cassandra-data/data
	commitlog_directory: /cassandra-server/commitlog
	saved_caches_directory: /cassandra-server/saved_caches
	- seeds: "75.126.183.212"
	listen_address: 75.126.183.212
	rpc_address: 75.126.183.212
	key_cache_size_in_mb: 8000
	key_cache_save_period: 86400
	row_cache_size_in_mb: 0
	row_cache_save_period: 0
	counter_cache_size_in_mb: 512
	counter_cache_save_period: 7200

##### Start Cassandra Instance

	:::text
	#vi ~/.bashrc
	#export PATH=$PATH:/cassandra-server/bin
	#export CQLSH_HOST=75.126.183.212
	#source ~/.bashrc
	#cassandra	

##### Confimr the Limits

To confirm the limits are applied to the Cassandra process, run the following command where pid is the process ID of the currently running Cassandra process:

	:::text
	$ cat /proc/<pid>/limits


Note : We have 3 Partitions with 500G on each Machine. We are taking /dev/sdb1 as a Cassandra-data and /dev/sdc1 as /social-log-dir and /dev/sdd1 as /collector-log-dir.

##### Create Director as /root/Cassandra-data/data

	:::text
	#mkdir Cassandra-data/data (all Cassandra data is available here)

1 /dev/sdb1 is mounted on /root/Cassandra-data/ directory and it contains one data folder. All Cassandra data is available on this director.
2. /dev/sdc1 is mounted on /social-log-dir Directory and it contains socialserver log and tvguide log.
3. /dev/sdb1 is mounted on collector-log-dir Directory and it contains all Collector Server log.
 

##### Verify the cassandra version

	:::text
	#cassandra -v

