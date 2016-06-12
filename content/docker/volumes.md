title: Docker Volumes
date: 2016-05-02
description: A tutorial on Docker
tags: docker, kubernets, spark, programming, hadoop, bigdata, yarn

Get Started with Volumes

In this lab we learn how to create a basic docker volume and mount it in a container

Volume mounted in a container

Execute the following command

$ docker run -v /volume1 -i -t ubuntu /bin/bash
This will mount /volume1 inside the container created from ubuntu image and launch and bash shell.

The command above will get us into the terminal tty of the container. Run ls command and you will notice volume 1 there

$root@b979b5d735b0:/# ls
bin  boot  dev  etc  home  lib  lib64..  var  volume1
On inspecting the docker container you will notice that /volume1 is mounted under / and is a ReadWrite Volume

{
     "Volumes": {
    "/volume1": "/var/lib/docker/vfs/dir/012..5a569b392"
    },
    "VolumesRW": {
    "/volume1": true
    }
 }
Mount a Host Directory as a Volume

Create a local directory /host/logs

$ sudo mkdir -p /host/logs
$ sudo touch /host/logs/log1.txt
Execute the following command to bind /host/logs host directory to /container/logs volume

$ docker run -v /host/logs:/container/logs -i -t ubuntu  /bin/bash
Execute ls to see the contents of mounted volume. Notice that contents are the same as created in host directory.

root@3774005dee32:/# ls
bin  boot  container  .. srv  sys  tmp  usr  var
root@3774005dee32:/# ls container/logs/
log1.txt


Volumes from Docker Image

Docker Image with Volume specified in Dockerfile

In this lab we look at

How to add a file as a volume using Dockerfile format.
Create an Image from the Dockerfile
Use the Image to create a container and check if the file exists.
Create the Dockerfile

Create a Dockerfile as shown below in a directory. Make sure file1 exists in the same directory. We are gong to mount file1 as /ubuntu1/file and mount /ubuntu1 as a VOLUME.

FROM ubuntu
ADD file1 /ubuntu1/file
VOLUME /ubuntu1
CMD /bin/sh
Create an Image from the Dockerfile

Execute the command below to build the image test/volume-one-dockerfile

docker build -t test/volume-one-dockerfile .
Create a Docker container

Create a container from the image test/volume-one-dockerfile

docker run -it test/volume-one-dockerfile
This command above will launch the bash shell of the container. Check if the volume /ubuntu1 is mounted

# ls
bin  boot  dev      etc  home  lib  .. sbin  srv  sys  tmp  ubuntu1  usr  var
# ls /ubuntu1
file
Docker Container with volume from Command Line and Image

In this section you will learn how to use command line to mount a host directory into a container created from an image

Create a Local directory

Create a local directory ubuntu2 and two files file1 and file2 in that directory.

$sudo mkdir -p /ubuntu2
[sudo] password for ubuntu:
$ sudo touch /ubuntu2/file1
$ sudo touch /ubuntu2/file2
Create a Container with a Volume ubuntu2

Create a container from the image :code:test/volume-one-dockerfile by specifying the directory to be mounted on the command line with a flag -v.

$ docker run -it -v /ubuntu2:/ubuntu2 test/volume-one-dockerfile
Check that the directory ubuntu2 got mounted in the docker container. Run ls in the container shell.

# ls
bin  boot  dev      etc  home  lib sys  tmp  ubuntu1  ubuntu2       usr  var
# ls ubuntu2
file1  file2
As you can see above both ubuntu1 and ubuntu2 got mounted as volumes.

[Ref]	https://blog.docker.com/2015/04/docker-tutorial-3-fun-with-volumes/
Container with ReadOnly Volume

Specify the :ro as shown below to make the volume readonly.

$ docker run -it -v /ubuntu2:/ubuntu2:ro test/volume-one-dockerfile
Try creating a new file in that volume from the bash shell of the container.

# touch /ubuntu2/file3
touch: cannot touch '/ubuntu2/file3': Read-only file system


Volumes From Another Container

Volumes from a container can be bound to another container using --volumes-from <container-name flag. Make sure there is host directory with contents /ubuntu1/code

$ ls /ubuntu1
file
Create a Container with a Volume Create a container with name ubuntu1 from image ubuntu

$ docker run -it --name ubuntu1 -v /ubuntu1:/ubuntu1 ubuntu
root@f031b82e5da6:/# ls ubuntu1
file
Create Second Container with shared volumes

Create a second container ubuntu2 with volumes from ubuntu1

$ docker run -it --name ubuntu2 --volumes-from ubuntu1 ubuntu
Note : -volumes-from is also valid but deprecated.

Check that the ubuntu1 volume is bound as expected

root@b28ca7033e9d:/# ls
bin  boot  dev  etc  home  ..  ubuntu1  usr  var
root@b28ca7033e9d:/# ls ubuntu1
file

