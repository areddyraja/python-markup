title: Docker Networking
date: 2016-05-02
description: A tutorial on Docker
tags: docker, kubernets, spark, programming, hadoop, bigdata, yarn

Bind Host Port to container Port

Make a docker file directory

$ mkdir docker-file
Make a docker file

$ cd docker-file/
$ touch Dockerfile
Add content to docker file

$ cat > Dockerfile
FROM ubuntu:14.04
MAINTAINER abc "abc@abc.com"
RUN apt-get update
RUN apt-get install -y nginx
RUN echo 'Our first Docker image for Nginx' > /usr/share/nginx/html/index.html
EXPOSE 80
Ctrl+D to save the changes

Create your own image

Build a docker image
$ sudo docker build -t="test/test_nginx_image" .
You will see output as shown below

Sending build context to Docker daemon 2.56 kB
Sending build context to Docker daemon
Step 0 : FROM ubuntu:14.04
---> 9cbaf023786c
Step 1 : MAINTAINER abc "abc@abc.com"
---> Using cache
---> 912452fdbe6d
Step 2 : RUN apt-get update
---> Using cache
---> d711127e4d76
Step 3 : RUN apt-get install -y nginx
---> Running in 4fab72b24686
Processing triggers for libc-bin (2.19-0ubuntu6.3) ...
Processing triggers for sgml-base (1.26+nmu4ubuntu1) ...
---> b9f58e96b137
Removing intermediate container 4fab72b24686
Step 4 : RUN echo 'Our first Docker image for Nginx' > /usr/share/nginx/html/index.html
---> Running in 1d1702c4dae4
---> c46b140fd8ad
Removing intermediate container 1d1702c4dae4
Step 5 : EXPOSE 80
---> Running in a98f7685870a
---> 728d805bd6d0
Removing intermediate container a98f7685870a
Successfully built 728d805bd6d0
Check that image has been created
$ docker images | grep nginx
test/test_nginx_image latest 1 day ago 2.433 MB
Run the newly created test-ngnix_image with port binding
$ sudo docker run -d -p 8080:80 --name test_container test/test_nginx_image nginx -g "daemon off;"
356389b43b02c5afb55de8145cb33a3e6539c671a97c2c6974a6308f1d7bac8d
The -p 8080:80 option will bind the host port 8080 to the container port 80. So we will be able to see the default web page of “Our first Docker image for Nginx” by simply visting the IP address of our docker host.

$ curl http://docker-host-ip:8080
Our first Docker image for Nginx





Using OVS bridge for docker networking

Install OVS

$ sudo apt-get install openvswitch-switch
Install ovs-docker utility

$ cd /usr/bin
$ wget https://raw.githubusercontent.com/openvswitch/ovs/master/utilities/ovs-docker
$ chmod a+rwx ovs-docker
Create an OVS bridge

Here we will be adding a new OVS bridge and configuring it, so that we can get the containers connected on the different network.

$ ovs-vsctl add-br ovs-br1
$ ifconfig ovs-br1 173.16.1.1 netmask 255.255.255.0 up
Add a port from OVS bridge to the Docker Container

Creat two ubuntu Docker Containers

$ docker run -t -i --name container1 ubuntu /bin/bash
$ docker run -t -i --name container2 ubuntu /bin/bash
Connect the container to OVS bridge

$ ovs-docker add-port ovs-br1 eth1 container1 --ipaddress=173.16.1.2/24
$ ovs-docker add-port ovs-br1 eth1 container2 --ipaddress=173.16.1.3/24
Test the connection between two containers connected via OVS bridge using Ping command

Extra configuration

If the containers are required to be connected to internet then a port is required to be added to the ethernet bridge of host which can be configured as per the command mentioned below. Please add an extra bridge eth1 so that we dont affect the present state of the host.

$ ovs-vsctl add-port ovs-br1 eth1



Weave Networking for Docker

Weave creates a virtual network that enables users to connect docker containers on different host and enable their auto-discovery

Install Weave

$ sudo wget -O /usr/local/bin/weave \
        https://github.com/weaveworks/weave/releases/download/latest_release/weave
$ sudo chmod a+x /usr/local/bin/weave
Launch weave containers

$ weave launch
This command will internally pull weave router container and run it

Start two application containers on weave network

$ C=$(weave run 10.2.1.1/24 -t -i ubuntu)
$ C12=$(weave run 10.2.1.2/24 -t -i ubuntu)
C and C12 hold the containerId of the containers created

$ echo $C
29e5ebaa8f0740077338a6d0d28d0760308f1a3ed2f39034392f1d278d96acd2
$ echo $C12
b0764f4e3792650c8664de2b601e00fc6dae211192dedbad36dcf1e0f11214c9
weave run command will internally run docker run -d command in order to set the ip address of weave network and start the ubuntu containers. Test the connection between two containers connected via weave network by using the ping command

$ docker attach $C
$ ping 10.2.1.2 -c 4
PING 10.2.1.2 (10.2.1.2) 56(84) bytes of data.
64 bytes from 10.2.1.2: icmp_seq=1 ttl=64 time=0.119 ms
64 bytes from 10.2.1.2: icmp_seq=2 ttl=64 time=0.152 ms
64 bytes from 10.2.1.2: icmp_seq=3 ttl=64 time=0.112 ms
64 bytes from 10.2.1.2: icmp_seq=4 ttl=64 time=0.104 ms

--- 10.2.1.2 ping statistics ---
4 packets transmitted, 4 received, 0% packet loss, time 2999ms
rtt min/avg/max/mdev = 0.104/0.121/0.152/0.022 ms

