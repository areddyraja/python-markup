Docker Images

Show images

$ sudo docker images
Specifying a Variant

$ sudo docker run -t -i ubuntu:14.04 /bin/bash
Pull an Image

$ sudo docker pull debian
Create your own image

Create a Dockerfile with the following content

FROM debian:wheezy

RUN apt-get update && apt-get install -y cowsay fortune
Go to the directory container Dockerfile and execute the following command to build a image

$ docker build -t test/cowsay-dockerfile .
You will see output as shown below

Sending build context to Docker daemon 2.048 kB
Sending build context to Docker daemon
Step 0 : FROM debian:wheezy
wheezy: Pulling from debian
7a3e804ed6c0: Pull complete
b96d1548a24e: Already exists

Status: Downloaded newer image for debian:wheezy
 ---> b96d1548a24e
Step 1 : RUN apt-get update && apt-get install -y cowsay fortune
 ---> Running in 4404353a3643
Get:1 http://security.debian.org wheezy/updates Release.gpg [1554 B]
Get:2 http://security.debian.org wheezy/updates Release [102 kB]
Get:3 http://httpredir.debian.org wheezy Release.gpg [2390 B]
.....
Setting up perl (5.14.2-21+deb7u2) ...
update-alternatives: using /usr/bin/prename to provide /usr/bin/rename
 ---> ca3618d10f2a
Removing intermediate container 4404353a3643
Successfully built ca3618d10f2a
Check that image has been created

$ docker images
REPOSITORY                   TAG                 IMAGE ID            CREATED             VIRTUAL SIZE
test/cowsay-dockerfile       latest              ca3618d10f2a        3 minutes ago       126.9 MB
docker-dev                   dry-run-test-2      db155754d7fc        6 days ago          1.571 GB
<none>                       <none>              b01392d005bb        6 days ago          1.571 GB
debian                       wheezy              b96d1548a24e        7 days ago          84.97 MB
debian                       latest              df2a0347c9d0        7 days ago          125.2 MB
dockerswarm/dind-master      latest              bb4cd757411e        7 days ago          159 MB
<none>                       <none>              f672d2db20f6        7 days ago          1.571 GB
<none>                       <none>              1fe07c1fdf52        8 days ago          1.571 GB
dockerswarm/swarm-test-env   latest              01e6a0da0825        2 weeks ago         515.5 MB
ubuntu                       14.04               07f8e8c5e660        3 weeks ago         188.3 MB
hello-world                  latest              91c95931e552        5 weeks ago         910 B
busybox                      latest              8c2e06607696        5 weeks ago         2.433 MB
Run the cowsay program using the built image

$ docker run test/cowsay-dockerfile /usr/games/cowsay "Hi!"
This will execute and show the output

 _____
< Hi! >
 -----
        \   ^__^
         \  (oo)\_______
            (__)\       )\/\
                ||----w |
                ||     ||
Removing a Docker Image : Docker image can be removed using the following command

$ docker rmi test/cowsay-dockerfile

