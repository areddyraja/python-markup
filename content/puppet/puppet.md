title: Puppet
date: 2016-05-02
description: Introduction to Puppet
tags: puppet, hiera, terraform, aws, provisioningo

Puppet is a configuration management tool that is extremely powerful in deploying, configuring, managing, maintaining, a server machine.
In other words you can say that puppet can be used for an entire life of a server, starting from bootstrapping a server, to shredding and giving up a server.

To give you an overview let me say that you can define distinct configuration for each and every host using puppet, and continuously check and confirm whether the required configuration is in place and is not altered(if altered puppet will revert back to the required configuration ) on the host.

Puppet keeps the configuration of your hosts under check, and can be used in one shot to configure a machine from scratch (like installing package, editing and configuring,create and mange users required) etc.
The main added advantage is that you can manage the configuration of almost all open-source tools available out there, using puppet.

Puppet is made by Luke Kanies. It is based on Ruby Language. Currently puppet is supported by Puppet Labs. 

Puppet supports most of the platforms including Windows.

The advantages of puppet are:
* Puppet keeps verifying the configuration at a specified interval
* Puppet defines the configurations of a host with the help of language which is easy to learn
* Puppet is used my major players in the industry including Google, Yahoo.
* Large open source developer base
* Support for a number of platforms
* Works smooth even if deployed with several hundreds of computers


### How it works
Puppet software comes with Puppet Master and Puppet Agent.

Puppet Master - The machine contains configuration for different hosts. Puppet Master will run as a daemon on this master server.
Puppet Agent - Puppet agent runs on all the servers, which are managed using Puppet. Puppet agents pulls the configuration from the puppet master at a regular intervals.

The connection between puppet master and server is made in a secure encrypted channel with the help of SSL.
TO DO Picture here

Puppet uses a tool called facter to support multiple platforms.
Using facter, the puppet agent gives complete details about the node to the puppet Master.
Facter providea a very rich information about the node.

Puppet master on getting the complete information from the node, take a decision with the help of the information provided and applies the configuration of that node.

Some of the simple things that can be done on the node is to apply an IP Adress, set hostname, configure gateway etc.

Facter is an important tool that puppet uses.
A sample facter output on a VM is shown below:

	:::test
	sudo facter
	architecture => x86_64
	augeasversion => 1.0.0
	bios_release_date => 12/01/2006
	bios_vendor => innotek GmbH
	bios_version => VirtualBox
	blockdevice_sda_model => VBOX HARDDISK
	blockdevice_sda_size => 21474836480
	blockdevice_sda_vendor => ATA
	blockdevices => sda
	boardmanufacturer => Oracle Corporation
	boardproductname => VirtualBox
	boardserialnumber => 0
	domain => dev.gfcp.io
	ec2_instance_id => local
	ec2_tag_environment => local
	ec2_tag_role => local
	ec2_tag_tier => local
	facterversion => 2.4.6
	filesystems => ext4,iso9660
	fqdn => gfcp-local.dev.gfcp.io
	gfcp_version => true
	gid => root
	hardwareisa => x86_64
	hardwaremodel => x86_64
	hostname => gfcp-local
	id => root
	include_apos => true
	interfaces => eth0,eth1,lo
	ipaddress => 10.0.2.15
	ipaddress_eth0 => 10.0.2.15
	ipaddress_eth1 => 172.16.1.2
	ipaddress_lo => 127.0.0.1
	is_vagrant => true
	is_virtual => true
	kernel => Linux
	kernelmajversion => 2.6
	kernelrelease => 2.6.32-642.1.1.el6.x86_64
	kernelversion => 2.6.32
	local_prefix => local_reddyraja
	macaddress => 08:00:27:49:06:FB
	macaddress_eth0 => 08:00:27:49:06:FB
	macaddress_eth1 => 08:00:27:8B:7D:2F
	manufacturer => innotek GmbH
	memoryfree => 4.85 GB
	memoryfree_mb => 4965.78
	memorysize => 7.69 GB
	memorysize_mb => 7870.48
	mtu_eth0 => 1500
	mtu_eth1 => 1500
	mtu_lo => 65536
	netmask => 255.255.255.0
	netmask_eth0 => 255.255.255.0
	netmask_eth1 => 255.255.255.0
	netmask_lo => 255.0.0.0
	network_eth0 => 10.0.2.0
	network_eth1 => 172.16.1.0
	network_lo => 127.0.0.0
	operatingsystem => CentOS
	operatingsystemmajrelease => 6
	operatingsystemrelease => 6.8
	os => {"release"=>{"minor"=>"8", "major"=>"6", "full"=>"6.8"}, "family"=>"RedHat", "name"=>"CentOS"}
	osfamily => RedHat
	partitions => {"sda1"=>{"uuid"=>"04018524-a7ad-485e-a07a-27b820c4c774", "mount"=>"/boot", "size"=>"1024000", "filesystem"=>"ext4"}, "sda2"=>{"size"=>"40916992", "filesystem"=>"LVM2_member"}}
	path => /usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin
	physicalprocessorcount => 1
	processor0 => Intel(R) Core(TM) i7-3615QM CPU @ 2.30GHz
	processor1 => Intel(R) Core(TM) i7-3615QM CPU @ 2.30GHz
	processorcount => 2
	processors => {"physicalcount"=>1, "count"=>2, "models"=>["Intel(R) Core(TM) i7-3615QM CPU @ 2.30GHz", "Intel(R) Core(TM) i7-3615QM CPU @ 2.30GHz"]}
	productname => VirtualBox
	project_home => /vagrant
	ps => ps -ef
	puppetversion => 3.8.7
	rubyplatform => x86_64-linux
	rubysitedir => /usr/lib/ruby/site_ruby/1.8
	rubyversion => 1.8.7
	selinux => true
	selinux_config_mode => permissive
	selinux_config_policy => targeted
	selinux_current_mode => permissive
	selinux_enforced => false
	selinux_policyversion => 24
	serialnumber => 0
	sshdsakey => AAAAB3NzaC1kc3MAAACBAOSOdC70GK+62b1DmmHw37vZ6VEUcQLv9AfkTvjcqOrKrTNGNMcY+fzJtbcfTG4i21YEDa8CSHoYtsrfZy4nLamc+CIclQONCXNR1W+jCXpe/mjY7V0p9JjKDsTMX+o9jFsuBNYLpPK5w/udoUvVEETET66Rffh7ylVdwrGsw72vAAAAFQCsxMUYvE0SSNELWgJeNZUl0MMxlwAAAIEAyssLRdOH4F0ijHHFbsQbreJSWpJSb7JMwOTVzECe97KfsoCV6VUuMBsTg/4GKWxHxK35z/VZSftPfFFaAtIERtStRfYlelZOZ0ftuc4+VZmQ4OWiOV2gBrWCUzPeo9BcFMWzeQEPpn2ZIabAn9lfdAzf/2dtYiZScgesW1DKG3MAAACADhQF5ON8mfbTUwEem0PvB9JER0cm8CE1qYCa6UFRVQNGr9UhTUC9+layi4U858Qi1W98UNavmogVc1mMiGlOODVQRUb0VTlUHRVVaFAANd4iW0n8Iy+fcaS6soDMYyw2UYwpFjHWeBE9Gf8ESg7aJVt14BJpQkVX/plsjWvGh5w=
	sshfp_dsa => SSHFP 2 1 0e9e8e299b19eb61dd5f9eea7b142f9ac7df2cd3
	SSHFP 2 2 03106abaacaa1af5103053b6e933bb603c933bb9ebc0f3d962ac9cc2ba35e37d
	sshfp_rsa => SSHFP 1 1 92e88fd08705813da6d5f9b7d5f79355282b9397
	SSHFP 1 2 58e36c85866db8936510aadd0785ef700c172dd1ecc2d30c4d52996fc53a8bac
	sshrsakey => AAAAB3NzaC1yc2EAAAABIwAAAQEA1aDd89yysGoH+u57JguOVc1HOAURwMzsyiE58Un4qdB6RWdfHbzx+hhaYMk6HpUU2pYcHpFL+RPNsXLWx6wH2e/HvRfOi1pHxElpX9P8Q1jwKDIgEzAVRhnTIejDw0MiKv8EVIXexcs8ZGrfcVh1eRSGlGUyJs+vY7MVbMlmL6cuz4mf70Gf55YRPCyXuubyicz9bthyClykHzR8PPjCYL/hXyNed69TqlC2/xDqOs5apK/ND5nytA4irCZGh3POABxapIAjcSYU3MR7VMpV5CbUoPaeW8Zvldbbdf41Hg0mScAAvutJNgdy6p5Wy/WLAa6otJ2RiVAYNP+l5sDz2Q==
	swapfree => 974.81 MB
	swapfree_mb => 974.81
	swapsize => 992.00 MB
	swapsize_mb => 992.00
	system_uptime => {"seconds"=>32704, "uptime"=>"9:05 hours", "hours"=>9, "days"=>0}
	timezone => UTC
	type => Other
	uniqueid => 007f0100
	uptime => 9:05 hours
	uptime_days => 0
	uptime_hours => 9
	uptime_seconds => 32704
	uuid => 48216504-7D2B-4A2A-8CF3-40164F63913A
	virtual => kvm

