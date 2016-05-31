title: Vagrant
date: 2016-05-02
description: Vagrant Tutorials
tags: Vagarant, docker, ruby, pupper, chef, Ansible, vagrantfile, guesadditions

##Overview
Vagrant is one of the manadatory tools that is emerging int the hands of the developer. A new and improved version called otto would be release by Hash Corp soon. The vagrant tools has become in the hands f the developer.

The primary purpose of Vagrant is to have a base box(virual) machine. On this base box, we can create all the additional software for customizations.
Vagrant provides the flexibility to control the provisioning of the software. The process becomes repeatitive and automatic.
Vagrant provides multiple options to provision custom software. It offers basic shell scripts to software automation managers like Puppet, Chef, Ansible. Multiple providers of VM can also be configured.

ihere is always an option to install all the software by doing ssh to the machine using vagrant ssh and provisiont the software red.

####Password less access to Vagrant
All of the operations carried out by Vagrant will use the vagrant user and all of the sudo commands need to execute without asking for a password each time they are ran.

To set this up we need to run the visudo command to configure password-less sudo for the user. Just type:

visudo
Add the following line to the end of the file and save it:

	:::shell
	vagrant ALL=(ALL) NOPASSWD:ALL

####List all Vagrant Plugin

	:::shell
	vagrant plugin list

####Install a Vagrant Plugin

	:::shell
	vagrant plugin install vagrant-vbguest

####Uninstall a vagrant pluing

	:::shell
	vagrant plugin uninstall vagrant-vbguest


####Installing Vagrant


####The Vagrantfile
Vagrantfile is the primary file where all the commands for Vagrant will be present.
The configuration syntax for the vagrantfile is Ruby, however does not require Ruby expertise.

#####Vagrant API Version
Vagrant uses API versions for its configuration file, this is how it can stay backwards compatible

	:::shell
	Vagrant.configure("2") do |config|
	end

#####Confiuring base box
This is the basic VM that needs to be configured. The base box VM is hosted on the Vagrant cloud.
Only name is required to specified, vagrant gets the base box automatically by using the name.

Simple base box configuration

	:::shell
	config.vm.box = "primalskill/ubuntu-trusty64"

#####Network configurations
Network configurations for the base box can be specified as below.

	:::shell
	config.vm.network :forwarded_port, guest: 80, host: 8931, auto_correct: true

The above lines suggests that you can access the port 80 on the virtual machine using the port 8931 on the host machine.
Auto correct lets vagrant handle the port collisions automatically.

####Syncing project files
Sharing files between the host and guest machine can be copied.
Sharing the files between these machines can be done through vagrant as shown below:

	:::shell
	config.vm.synced_folder "./", "/var/www", create: true, group: "www-data", owner: "www-data"

First argument is the host machine folder.
The second argument (/var/www) is the folder on the guest machine.
create: true specifies that if the target folder (/var/www) does not exist, then create it automatically.
group: “www-data” and owner: “www-data” specifies the owner and the group of the shared folder inside the VM. By default most web servers use www-data as the owner accessing the files, it’s a good practice to set the ownership to this user.


#####VirtualBox specific configurations
Now that we configured the network and synced folders, we should configure the virtual machine itself. Vagrant lets you dynamically modify the VM – you can change the name, memory, etc.

We can do this within the provider block, which in our case is virtualbox. So let’s create the block, set the name and memory:

	:::shell
	config.vm.provider "virtualbox" do |v|
	    v.name = "SitePoint Test Vagrant"
	    v.customize ["modifyvm", :id, "--memory", "1024"]
	end


Vagrant uses VBoxManage for setting VM specific parameters before booting it up. For more configuration parameters you can visit the VirtualBox VBoxManage documentation.

The :id is the virtual machine’s ID, which needs to be passed to VBoxManage everytime we want to modify something VM specific. Fortunately, Vagrant handles this for us, so we just need to pass this variable.

#####Shell script provisioning
The easiest way to provision a base box is to use basic shell script commands which then run inside the virtual machine. This also removes the need for learning or installing Puppet, Ansible and similar tools – even though they can sometimes be more effective provisioners. We’ll deal with them in future articles.

We need to define the provisioning type, which in our case is called shell. Let’s write that inside this block in the configuration file:

	:::shell
	config.vm.provision "shell" do |s|
	    s.path "provision/setup.sh"
	end

Vagrant has two types of shell provisioning, inline and external. With inline you can write shell commands in the Vagrantfile itself, but let’s focus on external provisioning, which simply means to load and run a shell script from a file (relative to Vagrantfile) or even from a URL.

In our case we want to load provision/setup.sh file, let’s create it and write the following in this file:

####Reloading
Reload the 

	:::shell
 	vagrant reload --provision-with puppet_server


####Forcing the provisioners to run
Now, run vagrant up and it will output Provisioning virtual machine… on the screen. 
Note that Vagrant will provision the virtual machine only once on the first run. 
The subsequent provisioning must be executed with the --provision flag either 
vagrant up --provision or vagrant reload --provision. 
The provisioning will re-run also if you destroy the VM and rebuild it with vagrant destroy and vagrant up.

Force the provisioners to run using the command

	:::shell
	vagrant reload --provision-with puppet-server 


####Installing Base Packages
Let the fun begin! Let’s install the base packages, namely: Git, Nginx, PHP-FPM and MySQL. In the provision/setup.sh file append the following lines:

echo "Installing Git"
    apt-get install git -y > /dev/null
    
    echo "Installing Nginx"
    apt-get install nginx -y > /dev/null
Simple as that, but while installing Git and Nginx is straightforward, this is not the case with PHP and MySQL, because each has specific configuration options.


####Acccess the VM

The following command gives the list of VMs running in the box

	:::shell
	vagrant status
	Current machine states:

	basebox                   not created (virtualbox)
	gfcpbox                   running (virtualbox)

The follwing command will allow to do ssh on the machine

	:::shell
	vagrant ssh box_name


####Provisioning
Provisioning happens at certain points during the lifetime of your Vagrant environment:

On the first vagrant up that creates the environment, provisioning is run. If the environment was already created and the up is just resuming a machine or booting it up, they will not run unless the --provision flag is explicitly provided.

* When vagrant provision is used on a running environment.
* The --provision flag must be present to force provisioning.
* When vagrant reload --provision is called. 
* You can also bring up your environment and explicitly not run provisioners by specifying --no-provision.
* Runs any configured provisioners against the running Vagrant managed machine.
This command is a great way to quickly test any provisioners, and is especially useful for incremental development of shell scripts, Chef cookbooks, or Puppet modules. You can just make simple modifications to the provisioning scripts on your machine, run a vagrant provision, and check for the desired results. Rinse and repeat.

* --provision-with x,y,z - This will only run the given provisioners. For example, if you have a :shell and :chef_solo provisioner and run vagrant provision --provision-with shell, only the shell provisioner will be run.


The command to run a specifc provisioner is as follows:

	:::shell
	vagrant provision --provision-with puppet_server


###Provisioing with a shared Puppet Server
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
