title: Installing Vagrant
date: 2016-05-02
description: A tutorial on Vagrant
tags: terraform, aws, provisioningo

The tutorial gives a basic steps in installing and running Vagrant

#### Download and Install Virtual Box

Download and install Virtual Box from the following site
https://www.virtualbox.org/

#### Download Vagrant
Download vagrant from below link
https://www.vagrantup.com/downloads.html
 
#### Install Vagrant
After installation, restart your system to get the variable setup
Otherwise move to the vagrant folder and then bin folder. press shift+right click. Click on open command line here.

#### Create Vagrant box
Change directory to /home/test/vagrant/vagrant/bin
(For Windows Change directory to C:\{vagrant_installed_dir}\bin

On the command prompt run the below commands: 

	:::text
	vagrant box add lucid32 http://files.vagrantup.com/lucid32.box
	vagrant init lucid32 
	vagrant up 
 
#### Login to Vagrant Box

Open Putty and enter these credentials:

	:::text
	Hostname: 127.0.0.1
	Port: 2222
	Connection type: SSH
	Enter username: vagrant
	Password: vagrant 

#### Login in thro Virtual Bx=ox

Open virtual box and login to the new VM with above credentials. 


