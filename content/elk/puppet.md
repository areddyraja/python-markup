title: Using Puppet to install Logstash, elastic search
date: 2016-05-02
description: A tutorial on Using Logstash and Kibana with Puppet
tags: terraform, aws, provisioningo

### Install puppet server and clients
#### Puppet Server

	:::text
	curl -s https://raw.githubusercontent.com/cloudwicklabs/scripts/master/puppet_install.sh | bash /dev/stdin -s -a -v

#### Puppet Client

	:::text
	curl -s https://raw.githubusercontent.com/cloudwicklabs/scripts/master/puppet_install.sh | bash /dev/stdin -c -H ${PUPPET_SERVER_HOST}

#### Install JDK

	:::text
	curl -L -C - -b "oraclelicense=accept-securebackup-cookie" \
	     -O http://download.oracle.com/otn-pub/java/jdk/7u45-b18/jdk-7u45-linux-x64.rpm

#### Elastic Search:
Install Elastic Search puppet module

	:::text
	puppet module install elasticsearch-elasticsearch
	
#### Configure ElasticSearch

	:::text
	node 'default' {
	  if versioncmp($::puppetversion,'3.6.1') >= 0 {

	    $allow_virtual_packages = hiera('allow_virtual_packages',false)

	    Package {
	      allow_virtual => $allow_virtual_packages,
	    }
	  }
	}

	node 'es.cloudwick.com' {
	  class { 'elasticsearch':
	    manage_repo  => true,
	    repo_version => '1.3',
	    config => { 'cluster.name' => 'logstash' }
	  }
	  # atleast one instance is required to start elasticsearch
	  elasticsearch::instance { 'es-01':
	    datadir => '/var/lib/elasticsearch/es-data-es01'
	  }
	}


#### Logstash:
Install Logstash puppet module

	:::text
	puppet module install elasticsearch-logstash

#### Configure Logstash

	:::text
	$config_hash = {
	 'LS_USER' => 'root',
	 'START' => 'true'
	}

	class { 'logstash':
	  install_contrib => true,
	  manage_repo  => true,
	  repo_version => '1.4',
	  init_defaults => $config_hash
	}

	logstash::configfile { 'configname':
	  content => template('logstash/final_config.erb')
	}

### Generate SSL Certificates

	:::text
	cd /etc/pki/tls; sudo openssl req -x509 -batch -nodes -days 3650 -newkey rsa:2048 -keyout private/logstash-forwarder.key -out certs/logstash-forwarder.crt

Place the configuration file in logstash module that we will be using:

	:::text
	cat > /etc/puppet/modules/logstash/templates/final_config.erb <<\EOF
	input {
	  lumberjack {
	    port => 5000
	    type => "syslog"
	    ssl_certificate => "/etc/pki/tls/certs/logstash-forwarder.crt"
	    ssl_key => "/etc/pki/tls/private/logstash-forwarder.key"
	  }
	  lumberjack {
	    port => 5001
	    type => "apache"
	    ssl_certificate => "/etc/pki/tls/certs/logstash-forwarder.crt"
	    ssl_key => "/etc/pki/tls/private/logstash-forwarder.key"
	  }
	  lumberjack {
	    port => 5002
	    type => "log4j"
	    ssl_certificate => "/etc/pki/tls/certs/logstash-forwarder.crt"
	    ssl_key => "/etc/pki/tls/private/logstash-forwarder.key"
	  }  
	}

	filter {
	  if [type] == "syslog" {
	    grok {
	      match => [ "message", "%{SYSLOGTIMESTAMP:syslog_timestamp} %{SYSLOGHOST:syslog_hostname} %{DATA:syslog_program}(?:\[%{POSINT:syslog_pid}\])?: %{GREEDYDATA:syslog_message}" ]
	      add_field => [ "received_at", "%{@timestamp}" ]
	      add_field => [ "received_from", "%{host}" ]
	    }
	    date {
	      match => [ "syslog_timestamp", "MMM  d HH:mm:ss", "MMM dd HH:mm:ss" ]
	    }
	  }
	  if [type] == "apache" {
	    grok {
	      patterns_dir => "/Users/lanyonm/logstash/patterns"
	      match => { "message" => "%{COMBINEDAPACHELOG}" }
	    }
	    date {
	      match => [ "timestamp", "dd/MMM/yyyy:HH:mm:ss Z" ]
	    }
	  }
	  if [type] == "log4j" {
	    multiline {
	      pattern => "(^\d+\serror)|(^.+Exception: .+)|(^\s+at .+)|(^\s+... \d+ more)|(^\s*Caused by:.+)"
	      what => "previous"
	    }
	    grep {
	      tags => [ "multiline" ]
	      add_field => [ "stacktrace", "true" ]
	    }
	    date {
	      match => [ "timestamp", "yyyy-MM-dd HH:mm:ss,SSS Z", "MMM dd, yyyy HH:mm:ss a" ]
	    }
	  }
	}

	output {
	  stdout {
	    codec => rubydebug
	  }
	  elasticsearch {
	    cluster => "logstash"
	  }
	}
	EOF

### Logstash forwarder
#### Install puppet module:

	:::text
	cd /etc/puppet/modules
	git clone https://github.com/elasticsearch/puppet-logstashforwarder.git logstashforwarder
	cd logstashforwarder
	cd templates
	curl -o logstash-forwarder http://logstashbook.com/code/4/logstash_forwarder_redhat_init

#### Configure logstash-forwarder

	:::text
	$config_hash_lsf = {
	 'LOGSTASH_FORWARDER_OPTIONS' => '"-config /etc/logstashforwarder/config.json -spool-size 100 -log-to-syslog"'
	}

	class { 'logstashforwarder':
	  manage_repo  => true,
	  servers  => [ 'logstash.yourdomain.com:5000' ],
	  ssl_ca   => '/etc/pki/tls/certs/logstash-forwarder.crt',
	  init_template => 'logstashforwarder/logstash-forwarder',
	  init_defaults => $config_hash_lsf
	}

	logstashforwarder::file { 'syslog':
	  paths  => [ '/var/log/messages', '/var/log/secure' ],
	  fields => { 'type' => 'syslog' }
	}

### Install and configure kibana
#### Download

	:::text
	cd /opt
	wget https://download.elasticsearch.org/kibana/kibana/kibana-3.1.0.tar.gz
	tar xzf kibana-3.1.0.tar.gz
	ln -s kibana-3.1.0 kibana

#### Configure Kibana

##### Install Nginx

	:::text
	rpm -Uvh http://download.fedoraproject.org/pub/epel/6/i386/epel-release-6-8.noarch.rpm
	yum -y install nginx

##### Configure Nginx to serve kibana

	:::text
	mkdir -p /usr/share/nginx/kibana3
	cp -R /opt/kibana/* /usr/share/nginx/kibana3/

##### Download sample nginx config:

	:::text
	cd ~; curl -OL https://github.com/elasticsearch/kibana/raw/master/sample/nginx.conf
	sed -i "s|server_name           kibana.myhost.org;|server_name $(hostname -f);|" nginx.conf
	sed -i "s|root  /usr/share/kibana3;|root /usr/share/nginx/kibana3;|" nginx.conf
	cp ~/nginx.conf /etc/nginx/conf.d/default.conf

##### Install apache2-utils to generate username and password pair (Optional)

	:::text
	yum -y install httpd-tools-2.2.15
	htpasswd -c /etc/nginx/conf.d/kibana.myhost.org.htpasswd admin



