title: Vagrant
date: 2016-05-02
description: Vagrant Tutorials
tags: Vagarant, docker, ruby, pupper, chef, Ansible, vagrantfile, guesadditions

##Provisioning with a shared Puppet Server
The following are the steps

* Decide the hostname
* Configure the node with the puppet
* Bring the box to manually provision
* Configure puupet master
* Create a Vagrant file
* Add a shell provisioner
* Add a puppet provisioner

#####Decide the hostname

	:::shell
	config.vm.hostname = "dev.example.co.uk"

#####Configure the node with the puppet

	:::shell
	node 'dev.example.co.uk' {
		  ...
		}



#####Bring the box to manually provision
Do this only once

	:::shell
	vagrant up
	vagrant ssh
	sudo puppet agent --no-daemonize --onetime --verbose --certname dev.example.co.uk --server
	puppetmaster.example.co.uk --detailed-exitcodes --waitforcert 60



#####Configure puupet master
	:::shell
	puppetca --sign dev.example.co.uk

	cat /etc/puppet/ssl/certs/dev.example.co.uk.pem
	cat /etc/puppet/ssl/private_keys/dev.example.co.uk.pem


And copy the contents of these files into two identical files within your local project. I suggest creating them within a directory structure such as this:

	:::shell
	/project_root/puppet_ssl/certs/dev.example.co.uk.pem
	/project_root/puppet_ssl/private_keys/dev.example.co.uk.pem


#####Share the certificates
Share the directory containing your puppet certificate and key:

	:::shell
	config.vm.synced_folder "./puppet_ssl", "/vagrant/puppet_ssl"

#####Add puppet provisioner

	:::shell
	config.vm.provision "puppet_server" do |puppet|
	puppet.puppet_server = "puppetmaster.example.co.uk"
	puppet.puppet_node = "dev.example.co.uk"
	puppet.options = "--no-daemonize --onetime --verbose"

#####Add a shell provisioner

	:::shell
	config.vm.provision "shell",
	  inline: "
	    mkdir -p /etc/puppet/ssl/certs;
	    mkdir -p /etc/puppet/ssl/private_keys;
	    cp /vagrant/puppet_ssl/certs/* /etc/puppet/ssl/certs;
	    cp /vagrant/puppet_ssl/private_keys/* /etc/puppet/ssl/private_keys"


#####Provision the VM

	:::shell
	vagrant up --provision

##Issues with Vagrant

####Issue: GuestAdditions versions on your host (5.0.10) and guest (5.0.4) do not match.

It looks like the iso file on your host machine is old.
The line Installing Virtualbox Guest Additions 5.0.4 refers to the version of the used installed script. This script was taken from your the /usr/share/virtualbox/VBoxGuestAdditions.iso.

Simply deleting /usr/share/virtualbox/VBoxGuestAdditions.iso should get rid of your immediate problem 

####Issue: Guest-specific operations were attempted on a machine that is not ready for guest communication

Removing this line in the Vgrantfile should work

	:::scala
	config.vbguest.auto_update = true"

or uninstall the plugin using the command.

	:::scala
	 vagrant plugin uninstall vagrant-vbguest




#####
References
1. http://www.sitepoint.com/vagrantfile-explained-setting-provisioning-shell/
2. http://vagrant-lists.github.io/  List of Vagrant plugins
