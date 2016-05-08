title: Docker Tutorials
date: 2016-05-02
description: Alpine Linux
tags: Alpine, Linux, docker, kubernets, spark, programming, hadoop, bigdata, yarn

###Getting Started with Alpine

Alpine is a lightweight linux distribution based on musl libc and busybox. There is a docker image based on Alpine which is an easy way of getting started with Alpine

####Alpine Docker Image

Based on Alpine kernel, this is a lightweight image of 5mb

####Pull the alpine image,

```
$ docker pull alpine
```
Check IP Address of the container

```
$ docker run alpine ifconfig
```
Launching a bash shell

```
$ docker run -i -t alpine /bin/bash
```
This will give an error, as bash is not supported in alpine

```
exec: "/bin/bash": stat /bin/bash: no such file or directory
docker: Error response from daemon: Container command not found or does not exist..
```
Getting inside the container

```
$ docker run -it alpine /bin/sh
/ #
Detaching from the container without stopping Ctrl-P Ctrl-Q
```

Check the docker container is still running

```
$ docker ps -a
CONTAINER ID        IMAGE                  COMMAND                  CREATED              STATUS                        PORTS                                           NAMES
8647ce2b84a5        alpine                 "/bin/sh"                About a minute ago   Up About a minute                                                             elegant_rosalind
```
