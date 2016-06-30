title: Puppet Configuration
date: 2016-05-02
description: Introduction to Puppet
tags: puppet, hiera, terraform, aws, provisioningo

Puppet.conf is the main configuration file for Puppet. The file is located in /etc/puppet directory.
This file gets created during the installation.

You can generate the file using the following command:

	:::text
	puppermasterd --genconfig > /etc/puppet/puppet.con

Puppet.conf file three main sections.

* [agent] -- this section is for mentioning agent specific parameters.
* [master] -- this section is for specifying options for puppet master.
* [main] -- this section will contain all global configuration options.

The following are the steps to start Puppet Master

#### Set up the FQDN for puppet

Puppet master generally addrssed by Fully Qualified Domain Name. To set

open the file /etc/hosts and add the following configuration

	:::text
	192.168.0.10 puppet puppet.sampledomain.com

add the DNS entry in the DNS.

#### Configuring Certificate

open the puppet.conf file and look for [master] section.

Add the following line to the section.

[master]
certname=puppet.sampledomain.com

#### Configuring site.pp file
site.pp tells the master what configurations to be applied to master.

The file is generally placed `/etc/puppet/manifests/` directory.

Create a file called site.pp inside the folder.

#### Manifests in puppet
Maniests are files that puppet calls as configuration files for the agent.
All the manifests files have the extension `.pp`

The location of these files can be altered using ` manifestdir and manifest` options in the puppet master file.

#### Directory where SSL resides in
The default directory for certificates is `/var/lib/puppet`

	:::text
	ls /var/lib/puppet/
	bucket        client_data  facts  reports  server_data  state
	clientbucket  client_yaml  lib    rrd      ssl          yaml

#### Starting Puppet Master

	:::text
	/etc/init.d/puppetmasterd start

OR

	:::text
	puppetmasterd

OR

	:::text
	puppet  master

For troubleshooting purposes you can run puppet master as the following.

	:::text
	puppet master --verbose --no-daemonize

Starting puppet master server will also create a self signed certificate for the master server which can be found at /var/lib/puppet/ssl/ca/signed/

	:::text
	ls /var/lib/puppet/ssl/ca/signed/
	puppet.sampledomain.com.pem

#### Configuring the puppet agent

Use the following command to connect to the pupper server on a node.

	:::text
	puppet agent --server puppet.sampledomain.com --no-daemonize --verbose

	:::text
	info: Creating a new SSL key for slashroot2.slashroot.in
	warning: peer certificate won't be verified in this SSL session
	info: Caching certificate for ca
	warning: peer certificate won't be verified in this SSL session
	warning: peer certificate won't be verified in this SSL session
	info: Creating a new SSL certificate request for puppet.sampledomain.com
	info: Certificate Request fingerprint (md5): 59:7A:AE:2C:7B:15:DA:E5:A8:14:7D:FF:1F:5B:7A:66
	warning: peer certificate won't be verified in this SSL session
	warning: peer certificate won't be verified in this SSL session
	warning: peer certificate won't be verified in this SSL session
	warning: peer certificate won't be verified in this SSL session
	<div style="display:none; visibility:hidden;" id="cosk"></div>
	notice: Did not receive certificate

As shown in the above example you can see that, an SSL key is made for this agent machine and is waiting for the corresponding certificate to be signed by the puppet master server.

An Important fact to note here is a notice shown in the above command result, which says that "notice: Did not receive certificate"

* --server in the above command specifies the puppet master server hostname
* --no-daemonize tells the puppet agent to not to run as a daemon, and also output the messages to the screen.

If you run puppet agent without this option, then you will not get the messages on the screen.

The ssl certificate signing is done only the first time an agent connects to the server.
The notice message(notice: Did not receive certificate)will keep on coming on the screen until the certificate request is signed by the puppet master.


On your puppet master run the below command to show the certificate signing requests.

	:::text
	puppetca --list
	  puppet.sampledomain.com (59:7A:AE:2C:7B:15:DA:E5:A8:14:7D:FF:1F:5B:7A:66)

puppet cert list command will also show you the same thing

Now lets sign the certificate by the following method.

	:::text
	puppetca --sign puppet.sampledomain.com
	notice: Signed certificate request for puppet.sampledomain.com
	notice: Removing file Puppet::SSL::CertificateRequest puppet.

Now as soon as the certificate gets signed from the master server you will get the below message on the puppet agent's screen(because we ran puppet agent command with --no-daemonize option on our agent). 

	:::text
	notice: Did not receive certificate
	warning: peer certificate won't be verified in this SSL session
	notice: Did not receive certificate

	warning: peer certificate won't be verified in this SSL session
	info: Caching certificate for slashroot2.slashroot.in
	notice: Starting Puppet client version 2.7.9
	info: Caching certificate_revocation_list for ca
	info: Caching catalog for puppet.sampledomain.com
	info: Applying configuration version '1355395673'
	info: Creating state file /var/lib/puppet/state/state.yaml
	notice: Finished catalog run in 0.14 seconds


It means that our puppet agent got a signed certificate and the certificate is cached. Also the agents tells us that its applying a configuration version number "1355395673" based on the catalog given by the master server.


We ran the command `puppet agent --server slashroot1.slashroot.in --no-daemonize --verbose`, just for showing the output on the screen as example.In normal cases you can add the puppet server address in the puppet.conf file of your agent machine.

So on our agent we will add server address in the [main] section as shown below.

server=puppet.sampledomain.com

After adding this server option in puppet.conf file simply restarting puppet agent will start it as a daemon. Which will periodically fetch data from the master server.
 
You can start/restart your puppet agent using the below commands.
 
	:::text
	/etc/init.d/puppet start
	 
	or
	 
	puppet agent


#### Getting started with manifests

Every node also called as the puppet client has got its configuration details defined in the puppet master server. The details(files,packages,configuration options) written in the language which puppet can understand is called as manifests. We will add some manifests for our node called "puppet-agent.sampledomain.com".

Puppet Server: puppet.sampledomain.com
Puppet Agent: puppet-agent.sampledomain.com

Manifest controls and define the configuration of the node. Manifests have the following things:

:::text
* Files.(these are the files which can be directly deployed on your puppet clients, for example httpd.con,yum.conf etc)
* Resources.
* Templates. (these can be used to construct configuration files on the node.)
* Nodes
* Resources
* Classes

The first and foremost thing before beginning our manifest, is to configure our site.pp file on the puppet master, which is under /etc/puppet/manifest/. 
Create the site.pp by following the following contents into site.pp

	:::text
	import 'nodes.pp'

	$puppetmaster = 'puppet.slashroot.in'

The import statement tells to import a file called nodes.pp. 
We have defined a variable called "puppetmaster" which can be used anywhere in our puppet manifest.


