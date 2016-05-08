title: Docker Tutorials
date: 2016-05-02
description: A tutorial on Docker
tags: docker, kubernets, spark, programming, hadoop, bigdata, yarn


###Getting Started

####Installation
Log into your Ubuntu installation as a user with sudo privileges.
Verify that you have wget installed.
$ which wget

```
If wget isn’t installed, install it after updating your manager:
$ sudo apt-get update $ sudo apt-get install wget
```

Get the latest Docker package.

```
$ wget -qO- https://get.docker.com/ | sh
```
The system prompts you for your sudo password.

Verify docker is installed correctly.
Execute the following command.

```
$ sudo docker run hello-world
```

You should see the following outout.

Hello from Docker.
This message shows that your installation appears to be working correctly.

To generate this message, Docker took the following steps:
 1. The Docker client contacted the Docker daemon.
 2. The Docker daemon pulled the "hello-world" image from the Docker Hub.
    (Assuming it was not already locally available.)
 3. The Docker daemon created a new container from that image which runs the
    executable that produces the output you are currently reading.
 4. The Docker daemon streamed that output to the Docker client, which sent it
    to your terminal.

To try something more ambitious, you can run an Ubuntu container with:
```
 $ docker run -it ubuntu bash
```
####Basic Commands

#####Info command

This command gives information about the docker setup on your machine/vm

```
$ docker info
```

Output of the command will look similar to the listing below

Containers: 0
Images: 301
Server Version: 1.9.0
Storage Driver: aufs
 Root Dir: /var/lib/docker/aufs
 Backing Filesystem: extfs
 Dirs: 301
 Dirperm1 Supported: false
Execution Driver: native-0.2
Logging Driver: json-file
Kernel Version: 3.13.0-32-generic
Operating System: Ubuntu 14.04.1 LTS
CPUs: 4
Total Memory: 3.141 GiB
Name: ubuntu
ID: CS3B:XJ7B:DEWA:NRXG:VGDY:HYWO:N4NA:FGXM:WYME:FW5C:WYJN:IHVJ
Username: rajdeepd
Registry: https://index.docker.io/v1/
WARNING: No swap limit support
Create a Container and enter its shell

```
$ sudo docker run -i -t debian /bin/bash
```

This should give you a new command prompt inside the container, very similar to if you had ssh‘ed into a remote machine. In this case the flags -i and -t tell Docker we want an interactive session with a tty attached. The command /bin/bash gives a bash shell. When you exit the shell the container will stop — containers only run as long as their main process

```
$ docker run debian echo hello-world
```
hello-world
Create a container with a name

You can use -h command line parameter to specify a container name.

```
$ docker run -h CONTAINER1 -i -t debian /bin/bash
```
Output of the command above will open a tty inside the container

root@CONTAINER1:/#
Create a container with a Networking mode

Container mode can be specified using the flag :code:`-net=<NETWORK_MODE> where

```
$ docker run -h CONTAINER2 -i -t --net="bridge" debian /bin/bash
```
List of docker containers running

```
$ docker ps -a
```
Inspect a Container

```
$ docker inspect hopeful_pare
```
Output will be a JSON file.

Start a Stopped Container

```
$ docker start hopeful_pare
```
where hopeful_pare is the container name.

Enter the Shell of a Started Container

```
$ docker attach hopeful_pare
```
where hopeful_pare is the container name.

Detach from a Container

```
docker run -t -i → can be detached with ^P^Q and reattached with docker attach
docker run -i    → cannot be detached with ^P^Q; will disrupt stdin
docker run       → cannot be detached with ^P^Q;
                   can SIGKILL client; can reattach with docker attach
```
Docker Logs

If you run this command with the name of your container, you should get a list of commands executed in the container.

```
$ docker logs hopeful_pare
```
where hopeful_pare is the container name.

Removing a Single Container

```
$ docker rm hopeful_pare
```
Removing all the Containers

```
$ docker rm `docker ps --no-trunc -aq`
```

