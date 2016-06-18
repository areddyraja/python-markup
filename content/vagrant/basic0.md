title: Vagrant
date: 2016-05-02
description: Very Basic one
tags: Vagarant, docker, ruby, pupper, chef, Ansible, vagrantfile, guesadditions

#### Boot a VM
The tutorial assumes that Virtual Box is already installed. 
Install Vagrant.

#### Initialize

To intialize type the followin command.

	:::text
	vagrant init ubuntu/trusty64

This creates a new file, Vagrantfile:

	:::text
	$ ls
	Vagrantfile

Now, using the Vagrantfile that was created, boot the box (“vagrant up”). 
If this is the first time, vagrant will first download the image from the cloud (could take a while):

	:::text
	vagrant up

When done with the booting up, SSH into the machine (“vagrant ssh”):

	:::text
	vagrant ssh

To destroy the box

Bring down the box (“vagrant destroy”). 

	:::text
	vagrant destroy

If this worked, let’s move on to installing some custom stuff on boot-up.

Runnig the shell script

Shell provisioning is a simple way to install stuff on “vagrant up”. 
First, let us create a shell script (“install.sh”) that we will later reference from the Vagrantfile. 
Furthermore, let’s live a little and install BrainFuck along with a hello world program.

open the file using

:::text
vi install.sh:

#!/bin/sh
sudo apt-get install bf
echo '++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++.' > helloworld.b

(Remember to “chmod 744” the install.sh script). Now, add a few lines of code to your Vagrantfile and you’re golden. After the edit, the file should look like this.

Vagrantfile:

	:::text
	# -*- mode: ruby -*-
	# vi: set ft=ruby :

	# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
	VAGRANTFILE_API_VERSION = "2"

	Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
	  config.vm.box = "ubuntu/trusty64"
	  config.vm.provision "shell", path: "install.sh"
	end

	Now, let’s test that it worked:

	:::text
	vagrant up
	vagrant ssh

	# now on virtual machine:
	$ bf helloworld.b
	Hello World!

