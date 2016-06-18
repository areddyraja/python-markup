title: Vagrant
date: 2016-05-02
description: Booting a Ubuntu VM
tags: Vagarant, docker, ruby, pupper, chef, Ansible, vagrantfile, guesadditions

### Booting a Ubuntu VM using vagrant

#### Config file
open Vagrantfile and copy the following contents:

	:::text
	vi Vagrantfile

	Vagrant.configure(2) do |config|
	  # Ubuntu 15.10
	  config.vm.box = "ubuntu/wily64"

	  config.vm.provider "virtualbox" do |vb|
	    # Display the VirtualBox GUI when booting the machine
	    vb.gui = true
	  end

	  # Install xfce and virtualbox additions
	  config.vm.provision "shell", inline: "sudo apt-get update"
	  config.vm.provision "shell", inline: "sudo apt-get install -y xfce4 virtualbox-guest-dkms virtualbox-guest-utils virtualbox-guest-x11"
	  # Permit anyone to start the GUI
	  config.vm.provision "shell", inline: "sudo sed -i 's/allowed_users=.*$/allowed_users=anybody/' /etc/X11/Xwrapper.config"
	end


You can change vb.gui = false to shutoff the Virtual Box user interface.


### Launch VM
Use the followig command to launch the VM

	:::text
	vagrant up

#### Login to VM
use ssh to login to VM

	:::text
	vagrant ssh

This should allow login without asking for password.

####  Destory VM
use the following command to destroy the VM
	
	:::text
	vagrant destory


#### Booting with Ubuntu UI 
"After installing the desktop, you'll also want to install GDM which will let you boot directly into a graphical environment. You'll also want to configure it."

Add the following lines to Vagrant file to launch the UI at boot time.

	:::text
	Vagrant::Config.run do |config|
	    config.vm.provision :shell, :inline => "sudo apt-get install gdm"
	    config.vm.provision :shell, :inline => "sudo dpkg-reconfigure gdm"
	end

####  Booting with two Monitors

The following script allows the VM to have to monitors.

	:::text
	Vagrant.configure(2) do |config|
	  config.vm.box = "box-cutter/ubuntu1404-desktop"

	  config.ssh.forward_agent = true

	  config.vm.network "forwarded_port", guest: 8080, host: 8080
	  config.vm.network "forwarded_port", guest: 3000, host: 3000


	  config.vm.synced_folder "../../git", "/home/vagrant/git"

	  config.vm.provider "virtualbox" do |vb|
	    vb.gui = true
	    vb.customize ["modifyvm", :id, "--monitorcount", "2"]
	    vb.memory = "2048"
	  end
	end

Note that, the VM's memory is also configured as part of the script.


