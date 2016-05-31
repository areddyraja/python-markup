title: Vagrant
date: 2016-05-02
description: Vagrant Tutorials
tags: Vagarant, docker, ruby, pupper, chef, Ansible, vagrantfile, guesadditions

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

