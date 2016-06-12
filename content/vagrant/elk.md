title: Logfile analysis with Logstash and Kibana
date: 2016-05-02
description: A tutorial on Using Logstash and Kibana
tags: terraform, aws, provisioningo

ELK( Elasticsearch, Logstash, Kibana ) 

#### Goal:
The goal of the tutorial is to set up Logstash to gather syslogs of multiple servers, and set up Kibana to visualize the gathered logs.

#### Introduction
Introducing ELK: Logstash is an open source tool for collecting, parsing, and storing logs for future use. Kibana 3 is a web interface that can be used to search and view the logs that Logstash has indexed. Both of these tools are based on Elasticsearch. Elasticsearch, Logstash, and Kibana, when used together is known as an ELK stack. 



#### Componentns
Our Logstash / Kibana setup has four main components:

* Logstash 1.4.2 --> The server component of Logstash that processes incoming logs. 
* Elasticsearch 1.1.1 --> Stores all of the logs.
* Kibana 3.0.1 --> Web interface for searching and visualizing logs.
* Logstash Forwarder 0.3.1 --> Installed on servers that will send their logs to Logstash, Logstash Forwarder serves as a log forwarding agent that utilizes the lumberjack networking protocol to communicate with Logstash. 

Let is install the first three components on a single server, which we will refer to as our Logstash Server.
The Logstash Forwarder will be installed on all of the servers that we want to gather logs for, which we will refer to collectively as our Servers. 

In addition to your Logstash Server, you will want to have a few other servers that you will gather logs from.

Let’s get started on setting up our Logstash Server! 

#### Install Java 8: 

Elasticsearch and Logstash require Java 8, so we will install that now. We will install OpenJDK 8.

Install the latest stable version of OpenJDK 8 with this command:

	:::text
	sudo yum -y install java-1.8.0-openjdk 

Now that Java 8 is installed, let’s install ElasticSearch. 

#### Install Elasticsearch: 

Note: Logstash 1.4.2 recommends Elasticsearch 1.1.1.

Run the following command to import the Elasticsearch public GPG key into rpm: 

	:::text
	sudo rpm --import http://packages.elasticsearch.org/GPG-KEY-elasticsearch 

#### Create and edit a new yum repository file for Elasticsearch: 

	:::text
	sudo vi /etc/yum.repos.d/elasticsearch.repo 

Add the following repository configuration:
 
	:::text
	[elasticsearch-1.1]
	name=Elasticsearch repository for 1.1.x packages
	baseurl=http://packages.elasticsearch.org/elasticsearch/1.1/centos
	gpgcheck=1
	gpgkey=http://packages.elasticsearch.org/GPG-KEY-elasticsearch
	enabled=1 

Save and exit. 

Install Elasticsearch 1.1.1 with this command: 

	:::text
	sudo yum -y install elasticsearch-1.1.1 

Elasticsearch is now installed. Let’s edit the configuration: 

	:::text
	sudo vi /etc/elasticsearch/elasticsearch.yml 

Add the following line somewhere in the file, to disable dynamic scripts: 
     
     script.disable_dynamic: true

You will also want to restrict outside access to your Elasticsearch instance, 
so outsiders can’t read your data or shutdown your Elasticseach cluster through the HTTP API. 
Find the line that specifiesnetwork.host and uncomment it so it looks like this: 

	:::text
	network.host: localhost 

Then disable multicast by finding the discovery.zen.ping.multicast.enabled item and uncommenting so it looks like this: 

	:::text
	discovery.zen.ping.multicast.enabled: false 

Save and exit elasticsearch.yml. 

#### Now start Elasticsearch: 

	:::text
	sudo service elasticsearch restart 

Then run the following command to start Elasticsearch on boot up: 
 
     $ sudo /sbin/chkconfig --add elasticsearch 

Now that Elasticsearch is up and running, let’s install Kibana. 

#### Install Kibana:  

  Note: Logstash 1.4.2 recommends Kibana 3.0.1.

##### Download Kibana to your home directory with the following command: 

	:::text
	cd ~; curl -O https://download.elasticsearch.org/kibana/kibana/kibana-3.0.1.tar.gz 

##### Extract Kibana archive with tar: 

	:::text
	tar xvf kibana-3.0.1.tar.gz 

##### Open the Kibana configuration file for editing: 

	:::text
	vi ~/kibana-3.0.1/config.js 

In the Kibana configuration file, find the line that specifies the elasticsearch server URL, and replace the port number (9200 by default) with 80: 

	:::text
	elasticsearch: "http://"+window.location.hostname+":80", 

We will be using Nginx to serve our Kibana installation, so let’s move the files into an appropriate location. 
Create a directory with the following command: 

	:::text
	sudo mkdir -p /usr/share/nginx/kibana3 

Now copy the Kibana files into your newly-created directory: 

	:::text
	sudo cp -R ~/kibana-3.0.1/* /usr/share/nginx/kibana3/ 

Before we can use the Kibana web interface, we have to install Nginx. Let’s do that now. 

#### Install Nginx: (1.6.3 Version)

Add the Yum repository that contains Nginx: 

	:::text
	sudo rpm -Uvh http://download.fedoraproject.org/pub/epel/6/i386/epel-release-6-8.noarch.rpm 

##### Use Yum to install Nginx: 

	:::text
	sudo yum -y install nginx 

##### Download the sample Nginx configuration from Kibana’s github repository to your home directory: 

	:::text
	cd ~; curl -OL https://gist.githubusercontent.com/thisismitch/2205786838a6a5d61f55/raw/f91e06198a7c455925f6e3099e3ea7c186d0b263/nginx.conf 

##### Open the sample configuration file for editing: 

	:::text
	vi nginx.conf 

##### Set the FQDN Name
Find and change the values of the server_name to your FQDN 
(or localhost if you aren’t using a domain name) and root to where we installed Kibana, so they look like the following entries: 

	:::text
	server_name FQDN;
	root  /usr/share/nginx/kibana3; 

Save and exit. Now copy it over your Nginx default server block with the following command: 

	:::text
	sudo cp ~/nginx.conf /etc/nginx/conf.d/default.conf 

##### install apache2-utils so we can use htpasswd to generate a username and password pair: 

	:::text
	sudo yum install httpd-tools-2.2.15 

Then generate a login that will be used in Kibana to save and share dashboards (substitute your own username):

	:::text
	sudo htpasswd -c /etc/nginx/conf.d/kibana.myhost.org.htpasswd <user name> 

Then enter a password and verify it. The htpasswd file just created is referenced in the Nginx configuration that you recently configured. 

##### Restart Nginx to put our changes into effect: 

	:::text
	sudo service nginx restart 

##### configure Nginx to start on boot: 

	:::text
	sudo chkconfig --levels 235 nginx on 

Kibana is now accessible via your FQDN or the public IP address of your Logstash Server 
i.e. http://logstash_server_public_ip/. 
If you go there in a web browser, you should see a Kibana welcome page which will allow you to 
view dashboards but there will be no logs to view because Logstash has not been set up yet. 
Let’s do that now. 

#### Install Logstash: 

The Logstash package shares the same GPG Key as Elasticsearch, and we already installed that public key, so let’s create and edit a new Yum repository file for Logstash: 

	:::text
	sudo vi /etc/yum.repos.d/logstash.repo 

Add the following repository configuration:  

	:::text
	[logstash-1.4]
	name=logstash repository for 1.4.x packages
	baseurl=http://packages.elasticsearch.org/logstash/1.4/centos
	gpgcheck=1
	gpgkey=http://packages.elasticsearch.org/GPG-KEY-elasticsearch
	enabled=1 

Save and exit. 

##### Install Logstash 1.4.2 with this command: 

	:::text
	sudo yum -y install logstash-1.4.2 

##### Configure Logstash 
Logstash is installed but it is not configured yet. 

#####Generate SSL Certificates: 
Since we are going to use Logstash Forwarder to ship logs from our Servers to our Logstash Server, 
we need to create an SSL certificate and key pair. 
The certificate is used by the Logstash Forwarder to verify the identity of Logstash Server.

Now you have two options for generating your SSL certificates. 
If you have a DNS setup that will allow your client servers to resolve the IP address of the Logstash Server, 
use Option 2. Otherwise, Option 1 will allow you to use IP addresses. 

1.  Option 1: IP Address 

If you don’t have a DNS setup—that would allow your servers, that you will gather logs from, to resolve the IP address of your Logstash Server—you will have to add your Logstash Server’s private IP address to thesubjectAltName (SAN) field of the SSL certificate that we are about to generate. To do so, open the OpenSSL configuration file: 

	:::text
	sudo vi /etc/pki/tls/openssl.cnf 

 Find the [ v3_ca ] section in the file, and add this line under it (substituting in the Logstash Server’s private IP address): 

	:::text
	subjectAltName = IP: logstash_server_private_ip 

	 Save and exit. 

 Now generate the SSL certificate and private key in the appropriate locations (/etc/pki/tls/), with the following commands: 

	:::text
	$ cd /etc/pki/tls
	$ sudo openssl req -config /etc/pki/tls/openssl.cnf -x509 -days 3650 -batch -nodes -newkey rsa:2048 -keyout private/logstash-forwarder.key -out certs/logstash-forwarder.crt 

The logstash-forwarder.crt file will be copied to all of the servers that will send logs to Logstash but we will do that a little later. 
Let’s complete our Logstash configuration. If you went with this option, skip option 2 and move on to Configure Logstash. 

2. Option 2: FQDN (DNS) 

If you have a DNS setup with your private networking, you should create an A record that contains the Logstash Server’s private IP address—this domain name will be used in the next command, to generate the SSL certificate. 
Alternatively, you can use a record that points to the server’s public IP address. 
Just be sure that your servers (the ones that you will be gathering logs from) will be able to resolve the domain name to your Logstash Server. 

Now generate the SSL certificate and private key, in the appropriate locations (/etc/pki/tls/…), with the following command (substitute in the FQDN of the Logstash Server): 

	:::text
	cd /etc/pki/tls
	sudo openssl req -subj '/CN=<^>logstash_server_fqdn/' -x509 -days 3650 -batch -nodes -newkey rsa:2048 -keyout private/logstash-forwarder.key -out certs/logstash-forwarder.crt 

The logstash-forwarder.crt file will be copied to all of the servers that will send logs to Logstash but we will do that a little later. Let’s complete our Logstash configuration. 

#### Configure Logstash: 

Logstash configuration files are in the JSON-format, and reside in /etc/logstash/conf.d. The configuration consists of three sections: inputs, filters, and outputs. 

Let’s create a configuration file called 01-lumberjack-input.conf and set up our “lumberjack” input (the protocol that Logstash Forwarder uses): 

	:::text
	sudo vi /etc/logstash/conf.d/01-lumberjack-input.conf 

##### Insert the following input configuration: 

	:::text
	   input {
	   lumberjack {
	     port => 5000
	     type => "logs"
	     ssl_certificate => "/etc/pki/tls/certs/logstash-forwarder.crt"
	     ssl_key => "/etc/pki/tls/private/logstash-forwarder.key"
	   }
	 } 

Save and quit. This specifies a lumberjack input that will listen on tcp port 5000, and it will use the SSL certificate and private key that we created earlier.

Now let’s create a configuration file called 10-syslog.conf, where we will add a filter for syslog messages: 

	:::text
	sudo vi /etc/logstash/conf.d/10-syslog.conf 

##### Insert the following syslog filter configuration: 

	:::text
	    filter {
	      if [type] == "syslog" {
		grok {
		  match => { "message" => "%{SYSLOGTIMESTAMP:syslog_timestamp} %{SYSLOGHOST:syslog_hostname} %{DATA:syslog_program}(?:\[%{POSINT:syslog_pid}\])?: %{GREEDYDATA:syslog_message}" }
		  add_field => [ "received_at", "%{@timestamp}" ]
		  add_field => [ "received_from", "%{host}" ]
		}
		syslog_pri { }
		date {
		  match => [ "syslog_timestamp", "MMM  d HH:mm:ss", "MMM dd HH:mm:ss" ]
		}
	      }
	    } 

Save and quit. This filter looks for logs that are labeled as “syslog” type (by a Logstash Forwarder), and it will try to use “grok” to parse incoming syslog logs to make it structured and query-able.

Lastly, we will create a configuration file called 30-lumberjack-output.conf: 

	:::text
	sudo vi /etc/logstash/conf.d/30-lumberjack-output.conf 

Insert the following output configuration: 

	:::text
	    output {
	      elasticsearch { host => localhost }
	      stdout { codec => rubydebug }
	    } 

Save and exit. This output basically configures Logstash to store the logs in Elasticsearch. 

With this configuration, Logstash will also accept logs that do not match the filter, but the data will not be structured (e.g. unfiltered Nginx or Apache logs would appear as flat messages instead of categorizing messages by HTTP response codes, source IP addresses, served files, etc.).

If you want to add filters for other applications that use the Logstash Forwarder input, be sure to name the files so they sort between the input and the output configuration (i.e. between 01 and 30). 
 
##### Restart Logstash to put our configuration changes into effect: 

	:::text
	sudo service logstash restart 

Now that our Logstash Server is ready, let’s move onto setting up Logstash Forwarder. 

   
#### Set Up Logstash Forwarder: 

Note: Do these steps for each server that you want to send logs to your Logstash Server. 


##### Copy SSL Certificate and Logstash Forwarder Package: 
    
On Logstash Server, copy the SSL certificate to Server (substitute with your own login): 

	:::text
	scp /etc/pki/tls/certs/logstash-forwarder.crt user@server_private_IP:/tmp  

Install Logstash Forwarder Package 
On Server, download the Logstash Forwarder RPM to your home directory:

	:::text
	$ cd ~; curl -O http://download.elasticsearch.org/logstash-forwarder/packages/logstash-forwarder-0.3.1-1.x86_64.rpm 

##### Install the Logstash Forwarder Package: 

	:::text
	sudo rpm -ivh ~/logstash-forwarder-0.3.1-1.x86_64.rpm 

##### Install the Logstash Forwarder init script, so it starts on bootup. We will use the init script provided by logstashbook.com: 

	:::text
	$ cd /etc/init.d/; sudo curl -o logstash-forwarder http://logstashbook.com/code/4/logstash_forwarder_redhat_init 
	$ sudo chmod +x logstash-forwarder 

The init script depends on a file called /etc/sysconfig/logstash-forwarder. 
A sample file is available to download: 

	:::text
	sudo curl -o /etc/sysconfig/logstash-forwarder http://logstashbook.com/code/4/logstash_forwarder_redhat_sysconfig 

Open it for editing: 

	:::text
	$ sudo vi /etc/sysconfig/logstash-forwarder 

And modify the LOGSTASH_FORWARDER_OPTIONS value so it looks like the following: 

	:::text
	LOGSTASH_FORWARDER_OPTIONS="-config /etc/logstash-forwarder -spool-size 100" 

Save and quit. 

##### Copy the SSL certificate 
Copy the SSS certificate into the appropriate location (/etc/pki/tls/certs): 

	:::text
	sudo cp /tmp/logstash-forwarder.crt /etc/pki/tls/certs/ 

##### Configure Logstash Forwarder: 

On Server, create and edit Logstash Forwarder configuration file, which is in JSON format: 

	:::text
	$ sudo vi /etc/logstash-forwarder 

Now add the following lines into the file, substituting in your Logstash Server’s private IP address forlogstash_server_private_IP: 

	:::text
	    {
	      "network": {
		"servers": [ "logstash_server_private_IP:5000" ],
		"timeout": 15,
		"ssl ca": "/etc/pki/tls/certs/logstash-forwarder.crt"
	      },
	      "files": [
		{
		  "paths": [
		    "/var/log/messages",
		    "/var/log/secure"
		   ],
		  "fields": { "type": "syslog" }
		}
	       ]
	    } 

Save and quit. This configures Logstash Forwarder to connect to your Logstash Server on port 5000 (the port that we specified an input for earlier), and uses the SSL certificate that we created earlier. The pathssection specifies which log files to send (here we specify messages and secure), and the type section specifies that these logs are of type “syslog* (which is the type that our filter is looking for). 

Note that this is where you would add more files/types to configure Logstash Forwarder to other log files to Logstash on port 5000. 

Now we will want to add the Logstash Forwarder service with chkconfig: 

	:::text
	$ sudo chkconfig --add logstash-forwarder 

##### Start Logstash Forwarder 
Start the Logstash Forwarder to put our changes into place: 

	:::text
	$ sudo service logstash-forwarder start 

Now Logstash Forwarder is sending messages and auth.log to your Logstash Server! Repeat this process for all of the other servers that you wish to gather logs for.  

##### Connect to Kibana: 

When you are finished setting up Logstash Forwarder on all of the servers that you want to gather logs for, let’s look at Kibana, the web interface that we installed earlier.  

In a web browser, go to the FQDN or public IP address of your Logstash Server. You should see a Kibana welcome page. 

Click on Logstash Dashboard to go to the premade dashboard. You should see a histogram with log events, with log messages below (if you don’t see any events or messages, one of your four Logstash components is not configured properly). 


