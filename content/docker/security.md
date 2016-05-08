Docker Security CIS Benchmark

The following tutorial is an extension of the Center for Internet Security (CIS) benchmark, CIS DOCKER 1.6 BENCHMARK V1.0.0 published by Pravin Goyal <pgoyal@vmware.com>, Staff Engineer, VMware. In this tutorial we will be covering all the important guidelines to run docker containers in secured environment.

Host Configuration

This section covers security recommendations that you should follow to prepare the host machine that you plan to use for executing containerized workloads. Securing the Docker host and following your infrastructure security best practices would build a solid and secure foundation for executing containerized workloads.

Keep Docker version up to date

By staying up to date on Docker updates, vulnerabilities in the Docker software can be mitigated. An educated attacker may exploit known vulnerabilities when attempting to attain access or elevate privileges. Not installing regular Docker updates may leave you with running vulnerable Docker software. It might lead to elevation privileges, unauthorized access or other security breaches.

$ docker version
Client:
 Version:      1.9.1
 API version:  1.21
 Go version:   go1.4.2
 Git commit:   a34a1d5
 Built:        Fri Nov 20 13:20:08 UTC 2015
 OS/Arch:      linux/amd64

Server:
 Version:      1.9.1
 API version:  1.21
 Go version:   go1.4.2
 Git commit:   a34a1d5
 Built:        Fri Nov 20 13:20:08 UTC 2015
 OS/Arch:      linux/amd64
Only allow trusted users to control Docker daemon

The Docker daemon currently requires ‘root’ privileges. A user added to the ‘docker’ group gives him full ‘root’ access rights. Hence, only verified users should be added to docker group.

$ useradd test

$ passwd test
Enter new UNIX password:
Retype new UNIX password:
passwd: password updated successfully

$ su test

test@ubuntu:/home/vkohli$ ls -l /etc/passwd
-rw-r--r-- 1 root root 2238 Nov 27 01:33 /etc/passwd

test@ubuntu:/home/vkohli$ docker ps
Cannot connect to the Docker daemon. Is the docker daemon running on this host?

$ usermod -G docker test

$ su test

$ docker ps
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
Audit Docker Daemon

Apart from auditing your regular Linux file system and system calls, audit Docker daemon as well. Docker daemon runs with ‘root’ privileges. It is thus necessary to audit its activities and usage;

$ apt-get install auditd
Reading package lists... Done
Building dependency tree
Reading state information... Done
The following extra packages will be installed:
  libauparse0
Suggested packages:
  audispd-plugins
The following NEW packages will be installed:
  auditd libauparse0
0 upgraded, 2 newly installed, 0 to remove and 50 not upgraded.
Need to get 227 kB of archives.
After this operation, 732 kB of additional disk space will be used.
Do you want to continue? [Y/n] Y
Get:1 http://us.archive.ubuntu.com/ubuntu/ wily/main libauparse0 amd64 1:2.4.2-1ubuntu1 [35.1 kB]
Get:2 http://us.archive.ubuntu.com/ubuntu/ wily/main auditd amd64 1:2.4.2-1ubuntu1 [192 kB]
Fetched 227 kB in 6s (35.2 kB/s)
Selecting previously unselected package libauparse0:amd64.
(Reading database ... 176489 files and directories currently installed.)
Preparing to unpack .../libauparse0_1%3a2.4.2-1ubuntu1_amd64.deb ...
Unpacking libauparse0:amd64 (1:2.4.2-1ubuntu1) ...
Selecting previously unselected package auditd.
Preparing to unpack .../auditd_1%3a2.4.2-1ubuntu1_amd64.deb ...
Unpacking auditd (1:2.4.2-1ubuntu1) ...
Processing triggers for man-db (2.7.4-1) ...
Processing triggers for ureadahead (0.100.0-19) ...
Processing triggers for systemd (225-1ubuntu9) ...
Setting up libauparse0:amd64 (1:2.4.2-1ubuntu1) ...
Setting up auditd (1:2.4.2-1ubuntu1) ...
update-rc.d: warning: start and stop actions are no longer supported; falling back to defaults
Processing triggers for libc-bin (2.21-0ubuntu4) ...
Processing triggers for ureadahead (0.100.0-19) ...
Processing triggers for systemd (225-1ubuntu9) ...
Remove the audit log file if exist;

$ cd /etc/audit/

$ ls
audit.log

$ nano audit.log

$ rm -rf audit.log
Add the audit rules for docker service and audit the docker service;

$ nano audit.rules
-w /usr/bin/docker -k docker

$ service auditd restart

$ ausearch -k docker
<no matches>

$ docker ps
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES

$ ausearch -k docker
----
time->Fri Nov 27 02:29:50 2015
type=PROCTITLE msg=audit(1448620190.716:79): proctitle=646F636B6572007073
type=PATH msg=audit(1448620190.716:79): item=1 name="/lib64/ld-linux-x86-64.so.2" inode=398512 dev=08:01 mode=0100755 ouid=0 ogid=0 rdev=00:00 nametype=NORMAL
type=PATH msg=audit(1448620190.716:79): item=0 name="/usr/bin/docker" inode=941134 dev=08:01 mode=0100755 ouid=0 ogid=0 rdev=00:00 nametype=NORMAL
type=CWD msg=audit(1448620190.716:79):  cwd="/etc/audit"
type=EXECVE msg=audit(1448620190.716:79): argc=2 a0="docker" a1="ps"
type=SYSCALL msg=audit(1448620190.716:79): arch=c000003e syscall=59 success=yes exit=0 a0=ca1208 a1=c958c8 a2=c83008 a3=58c items=2 ppid=5203 pid=10863 auid=4294967295 uid=0 gid=0 euid=0 suid=0 fsuid=0 egid=0 sgid=0 fsgid=0 tty=pts2 ses=4294967295 comm="docker" exe="/usr/bin/docker" key="docker"



Host Configuration

This section covers security recommendations that you should follow to prepare the host machine that you plan to use for executing containerized workloads. Securing the Docker host and following your infrastructure security best practices would build a solid and secure foundation for executing containerized workloads.

Keep Docker version up to date

By staying up to date on Docker updates, vulnerabilities in the Docker software can be mitigated. An educated attacker may exploit known vulnerabilities when attempting to attain access or elevate privileges. Not installing regular Docker updates may leave you with running vulnerable Docker software. It might lead to elevation privileges, unauthorized access or other security breaches.

$ docker version
Client:
 Version:      1.9.1
 API version:  1.21
 Go version:   go1.4.2
 Git commit:   a34a1d5
 Built:        Fri Nov 20 13:20:08 UTC 2015
 OS/Arch:      linux/amd64

Server:
 Version:      1.9.1
 API version:  1.21
 Go version:   go1.4.2
 Git commit:   a34a1d5
 Built:        Fri Nov 20 13:20:08 UTC 2015
 OS/Arch:      linux/amd64
Only allow trusted users to control Docker daemon

The Docker daemon currently requires ‘root’ privileges. A user added to the ‘docker’ group gives him full ‘root’ access rights. Hence, only verified users should be added to docker group.

$ useradd test

$ passwd test
Enter new UNIX password:
Retype new UNIX password:
passwd: password updated successfully

$ su test

test@ubuntu:/home/vkohli$ ls -l /etc/passwd
-rw-r--r-- 1 root root 2238 Nov 27 01:33 /etc/passwd

test@ubuntu:/home/vkohli$ docker ps
Cannot connect to the Docker daemon. Is the docker daemon running on this host?

$ usermod -G docker test

$ su test

$ docker ps
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
Audit Docker Daemon

Apart from auditing your regular Linux file system and system calls, audit Docker daemon as well. Docker daemon runs with ‘root’ privileges. It is thus necessary to audit its activities and usage;

$ apt-get install auditd
Reading package lists... Done
Building dependency tree
Reading state information... Done
The following extra packages will be installed:
  libauparse0
Suggested packages:
  audispd-plugins
The following NEW packages will be installed:
  auditd libauparse0
0 upgraded, 2 newly installed, 0 to remove and 50 not upgraded.
Need to get 227 kB of archives.
After this operation, 732 kB of additional disk space will be used.
Do you want to continue? [Y/n] Y
Get:1 http://us.archive.ubuntu.com/ubuntu/ wily/main libauparse0 amd64 1:2.4.2-1ubuntu1 [35.1 kB]
Get:2 http://us.archive.ubuntu.com/ubuntu/ wily/main auditd amd64 1:2.4.2-1ubuntu1 [192 kB]
Fetched 227 kB in 6s (35.2 kB/s)
Selecting previously unselected package libauparse0:amd64.
(Reading database ... 176489 files and directories currently installed.)
Preparing to unpack .../libauparse0_1%3a2.4.2-1ubuntu1_amd64.deb ...
Unpacking libauparse0:amd64 (1:2.4.2-1ubuntu1) ...
Selecting previously unselected package auditd.
Preparing to unpack .../auditd_1%3a2.4.2-1ubuntu1_amd64.deb ...
Unpacking auditd (1:2.4.2-1ubuntu1) ...
Processing triggers for man-db (2.7.4-1) ...
Processing triggers for ureadahead (0.100.0-19) ...
Processing triggers for systemd (225-1ubuntu9) ...
Setting up libauparse0:amd64 (1:2.4.2-1ubuntu1) ...
Setting up auditd (1:2.4.2-1ubuntu1) ...
update-rc.d: warning: start and stop actions are no longer supported; falling back to defaults
Processing triggers for libc-bin (2.21-0ubuntu4) ...
Processing triggers for ureadahead (0.100.0-19) ...
Processing triggers for systemd (225-1ubuntu9) ...
Remove the audit log file if exist;

$ cd /etc/audit/

$ ls
audit.log

$ nano audit.log

$ rm -rf audit.log
Add the audit rules for docker service and audit the docker service;

$ nano audit.rules
-w /usr/bin/docker -k docker

$ service auditd restart

$ ausearch -k docker
<no matches>

$ docker ps
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES

$ ausearch -k docker
----
time->Fri Nov 27 02:29:50 2015
type=PROCTITLE msg=audit(1448620190.716:79): proctitle=646F636B6572007073
type=PATH msg=audit(1448620190.716:79): item=1 name="/lib64/ld-linux-x86-64.so.2" inode=398512 dev=08:01 mode=0100755 ouid=0 ogid=0 rdev=00:00 nametype=NORMAL
type=PATH msg=audit(1448620190.716:79): item=0 name="/usr/bin/docker" inode=941134 dev=08:01 mode=0100755 ouid=0 ogid=0 rdev=00:00 nametype=NORMAL
type=CWD msg=audit(1448620190.716:79):  cwd="/etc/audit"
type=EXECVE msg=audit(1448620190.716:79): argc=2 a0="docker" a1="ps"
type=SYSCALL msg=audit(1448620190.716:79): arch=c000003e syscall=59 success=yes exit=0 a0=ca1208 a1=c958c8 a2=c83008 a3=58c items=2 ppid=5203 pid=10863 auid=4294967295 uid=0 gid=0 euid=0 suid=0 fsuid=0 egid=0 sgid=0 fsgid=0 tty=pts2 ses=4294967295 comm="docker" exe="/usr/bin/docker" key="docker"


Docker Daemon Configuration

Docker daemon options can also be controlled using files such as /etc/sysconfig/docker or /etc/default/docker on Ubuntu. Also, note that Docker in daemon mode can be identified as having ‘-d’ as the argument to docker service.

Restrict network traffic between containers

By default, unrestricted network traffic is enabled between all containers on the same host. Thus, each container has the potential of reading all packets across the container network on the same host. This might lead to unintended and unwanted disclosure of information to other containers. Hence, restrict the inter container communication.

Create a nginx container;

$ docker run -d -p 4915:80 nginx
Unable to find image 'nginx:latest' locally
latest: Pulling from library/nginx
1565e86129b8: Pull complete
a604b236bcde: Pull complete
84cef7523477: Pull complete
fd07be91d48e: Pull complete
fb36adbd81bf: Pull complete
097ca86c0784: Pull complete
8e0912ce0c1b: Pull complete
306fa48b674e: Pull complete
e51a2e0cfd66: Pull complete
8ccac0b28146: Pull complete
20ea32821467: Pull complete
198a73cfd686: Pull complete
Digest: sha256:a3e3180ab6ac4a3095cf6d6225223e10fa5f5ac1b20939a4ba1d777918f63f9f
Status: Downloaded newer image for nginx:latest
39fc070bf79d1668580829a7b0bae125ec7e1812fae229246466358e29002579


$ curl http://localhost:4915
<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
<style>
    body {
        width: 35em;
        margin: 0 auto;
        font-family: Tahoma, Verdana, Arial, sans-serif;
    }
</style>
</head>
<body>
<h1>Welcome to nginx!</h1>
<p>If you see this page, the nginx web server is successfully installed and
working. Further configuration is required.</p>
<p>For online documentation and support please refer to
<a href="http://nginx.org/">nginx.org</a>.<br/>
Commercial support is available at
<a href="http://nginx.com/">nginx.com</a>.</p>
<p><em>Thank you for using nginx.</em></p>
</body>
</html>

$ docker ps
CONTAINER ID        IMAGE               COMMAND                  CREATED              STATUS              PORTS                           NAMES
39fc070bf79d        nginx               "nginx -g 'daemon off"   About a minute ago   Up About a minute   443/tcp, 0.0.0.0:4915->80/tcp   stupefied_mccarthy
Get the IP adress of nginx container.

$ docker inspect --format '{{  .NetworkSettings.IPAddress }}' 39f
172.17.0.2
Create a new centos container and try to ping the nginx container from it;

$ docker run -it centos bash
Unable to find image 'centos:latest' locally
latest: Pulling from library/centos
fa5be2806d4c: Pull complete
0cd86ce0a197: Pull complete
e9407f1d4b65: Pull complete
c9853740aa05: Pull complete
e9fa5d3a0d0e: Pull complete
Digest: sha256:c96eeb93f2590858b9e1396e808d817fa0ba4076c68b59395445cb957b524408
Status: Downloaded newer image for centos:latest
[root@df006460c9d1 /]# ping 172.17.0.2
PING 172.17.0.2 (172.17.0.2) 56(84) bytes of data.
64 bytes from 172.17.0.2: icmp_seq=1 ttl=64 time=0.147 ms
64 bytes from 172.17.0.2: icmp_seq=2 ttl=64 time=0.084 ms
64 bytes from 172.17.0.2: icmp_seq=3 ttl=64 time=0.109 ms
^C
--- 172.17.0.2 ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 1998ms
rtt min/avg/max/mdev = 0.084/0.113/0.147/0.027 ms
[root@df006460c9d1 /]# exit
exit
Now we will disbale the inter-communication between the containers by setting the –icc flag as false.

$ service docker stop

$ docker -d -icc=false &
[1] 12482
Warning: '-d' is deprecated, it will be removed soon. See usage.
Warning: '-icc' is deprecated, it will be replaced by '--icc' soon. See usage.
WARN[0000] please use 'docker daemon' instead.
INFO[0000] API listen on /var/run/docker.sock
INFO[0001] [graphdriver] using prior storage driver "aufs"
INFO[0003] Firewalld running: false
INFO[0003] Default bridge (docker0) is assigned with an IP address 172.17.0.1/16. Daemon option --bip can be used to set a preferred IP address
WARN[0003] Your kernel does not support swap memory limit.
INFO[0004] Loading containers: start.
......
INFO[0004] Loading containers: done.
INFO[0004] Daemon has completed initialization
INFO[0004] Docker daemon                                 commit=a34a1d5 execdriver=native-0.2 graphdriver=aufs version=1.9.1

$ docker ps
INFO[0017] GET /v1.21/containers/json
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
We will create both the containers again and we can check that they are not pingable.

$ docker run -d -p 4915:80 nginx
INFO[0088] POST /v1.21/containers/create
34e34a5354977206b358e305c08a152f5146b6126a94175639e35579f6a68571
INFO[0088] POST /v1.21/containers/34e34a5354977206b358e305c08a152f5146b6126a94175639e35579f6a68571/start
INFO[0090] No non-localhost DNS nameservers are left in resolv.conf. Using default external servers : [nameserver 8.8.8.8 nameserver 8.8.4.4]
INFO[0090] IPv6 enabled; Adding default IPv6 external servers : [nameserver 2001:4860:4860::8888 nameserver 2001:4860:4860::8844]

$ docker ps
INFO[0102] GET /v1.21/containers/json
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                           NAMES
34e34a535497        nginx               "nginx -g 'daemon off"   14 seconds ago      Up 10 seconds       443/tcp, 0.0.0.0:4915->80/tcp   drunk_franklin

$ docker inspect --format '{{  .NetworkSettings.IPAddress }}' 34e
INFO[0134] GET /v1.21/containers/34e/json
172.17.0.2

$ docker run -it centos bashINFO[0166] POST /v1.21/containers/create
INFO[0167] POST /v1.21/containers/08c82f15168a846037f1aa4ef2d0f16cb8757fa2e1754f07e2155a25024a174e/attach?stderr=1&stdin=1&stdout=1&stream=1
INFO[0167] POST /v1.21/containers/08c82f15168a846037f1aa4ef2d0f16cb8757fa2e1754f07e2155a25024a174e/start
INFO[0167] No non-localhost DNS nameservers are left in resolv.conf. Using default external servers : [nameserver 8.8.8.8 nameserver 8.8.4.4]
INFO[0167] IPv6 enabled; Adding default IPv6 external servers : [nameserver 2001:4860:4860::8888 nameserver 2001:4860:4860::8844]
INFO[0169] POST /v1.21/containers/08c82f15168a846037f1aa4ef2d0f16cb8757fa2e1754f07e2155a25024a174e/resize?h=24&w=80
[root@08c82f15168a /]# ping 172.17.0.2
PING 172.17.0.2 (172.17.0.2) 56(84) bytes of data.
^C
--- 172.17.0.2 ping statistics ---
4 packets transmitted, 0 received, 100% packet loss, time 3024ms
Do not bind Docker to another IP/Port or a Unix socket

By default, Docker daemon binds to a non-networked Unix socket and runs with ‘root’ privileges. If you change the default docker daemon binding to a TCP port or any other Unix socket, anyone with access to that port or socket can have full access to Docker daemon and in turn to the host system. Hence, you should not bind the Docker daemon to another IP/Port or a Unix socket.

Stop the docker service and then try to run it on different port which can be vulnerable.

$ docker -H tcp://0.0.0.0:2375 -H unix:///var/run/example.sock -d
Warning: '-d' is deprecated, it will be removed soon. See usage.
WARN[0000] please use 'docker daemon' instead.
WARN[0000] /!\ DON'T BIND ON ANY IP ADDRESS WITHOUT setting -tlsverify IF YOU DON'T KNOW WHAT YOU'RE DOING /!\
INFO[0000] API listen on [::]:2375
INFO[0000] [graphdriver] using prior storage driver "aufs"
INFO[0000] API listen on /var/run/example.sock
INFO[0000] Firewalld running: false
INFO[0000] Default bridge (docker0) is assigned with an IP address 172.17.0.1/16. Daemon option --bip can be used to set a preferred IP address
WARN[0000] Your kernel does not support swap memory limit.
INFO[0001] Loading containers: start.
..........
INFO[0001] Loading containers: done.
INFO[0001] Daemon has completed initialization
INFO[0001] Docker daemon                                 commit=a34a1d5 execdriver=native-0.2 graphdriver=aufs version=1.9.1
In new terminal check that -H option is present which should not exist during the default run of the docker service. After this tutorial, restart the default docker service.

$ ps -ef | grep docker



Docker Daemon Configuration Files

This section covers Docker related files and directory permissions and ownership. Keeping the files and directories, that may contain sensitive parameters, secure is important for correct and secure functioning of Docker daemon.

Verify that docker.socket file ownership is set to root:root

If you are using Docker on a machine that uses systemd to manage services, then verify that the ‘docker.service’ file ownership and group-ownership is correctly set to ‘root’.So that when the account is switched to test user he is not able to access the docker daemon as he is not authorized to do so by root account.

$ stat -c %U:%G /usr/lib/docker | grep -v root:root
$ stat -c %U:%G /usr/lib/docker | grep root:root
root:root
If the permission is not set to root:root then it can be changed by using the following command;

$ chown root:root /usr/lib/systemd/system/docker.service
$ su test
$ docker ps
Cannot connect to the Docker daemon. Is the docker daemon running on this host?
test@ubuntu:/etc/init.d$
Verify that docker.socket file permissions are set to 644 or more restrictive 660

If you are using Docker on a machine that uses systemd to manage services, then verify that the ‘docker.service’ file permissions are correctly set to ‘644’ or more restrictive.

As it can be seen below if we allocate 666 as the permission then the “test” user will be also be available to access the Docker daemon;

$ ls -l /var/run/docker.sock
srw-rw---- 1 root docker 0 Nov 27 05:56 /var/run/docker.sock
$ chmod 666 /var/run/docker.sock
$ su test
test@ubuntu:/etc/init.d$ docker ps
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
test@ubuntu:/etc/init.d$
As soon as we change the permission to 660 we will be able to see that the “test” user is not able to access the docker daemon.

$ chmod 660 /var/run/docker.sock
$ su test
test@ubuntu:/etc/init.d$ docker ps
Cannot connect to the Docker daemon. Is the docker daemon running on this host?
test@ubuntu:/etc/init.d$ exit
exit

Container Runtime

The ways in which a container is started governs a lot security implications. It is possible to provide potentially dangerous runtime parameters that might compromise the host and other containers on the host. Verifying container runtime is thus very important. Various recommendations to assess the container runtime are as below:

Do not use privileged containers

Docker supports the addition and removal of capabilities, allowing use of a non-default profile. This may make Docker more secure through capability removal, or less secure through the addition of capabilities. It is thus recommended to remove all capabilities except those explicitly required for your container process.

As seen below when we run the container without the privileged mode, we are unable to change the Kernel parameters but when we run the container in privileged mode using the -privileged flag it is able to change the Kernel Parameters easily, which can cause security vulnerability.

$ docker run -it centos /bin/bash
[root@7e1b1fa4fb89 /]#  sysctl -w net.ipv4.ip_forward=0
sysctl: setting key "net.ipv4.ip_forward": Read-only file system


$ docker run --privileged -it centos /bin/bash
[root@930aaa93b4e4 /]#  sysctl -a | wc -l
sysctl: reading key "net.ipv6.conf.all.stable_secret"
sysctl: reading key "net.ipv6.conf.default.stable_secret"
sysctl: reading key "net.ipv6.conf.eth0.stable_secret"
sysctl: reading key "net.ipv6.conf.lo.stable_secret"
638
[root@930aaa93b4e4 /]# sysctl -w net.ipv4.ip_forward=0
net.ipv4.ip_forward = 0
So, while auditing it should be made sure that all the containers should not have the privileged mode set to true.

$ docker ps -q | xargs docker inspect --format '{{ .Id }}: Privileged={{ .HostConfig.Privileged }}'
930aaa93b4e44c0f647b53b3e934ce162fbd9ef1fd4ec82b826f55357f6fdf3a: Privileged=true
Do not use host network mode on container

This is potentially dangerous. It allows the container process to open low-numbered ports like any other root process. It also allows the container to access network services like Dbus on the Docker host. Thus, a container process can potentially do unexpected things such as shutting down the Docker host. You should not use this option.

When we run the container with network mode as host, it will be able to change all the network configurations of the host which can cause a potential danger to the other running applications.

$ docker run -it --net=host ubuntu /bin/bash
$ ifconfig
docker0   Link encap:Ethernet  HWaddr 02:42:1d:36:0d:0d
          inet addr:172.17.0.1  Bcast:0.0.0.0  Mask:255.255.0.0
          inet6 addr: fe80::42:1dff:fe36:d0d/64 Scope:Link
          UP BROADCAST MULTICAST  MTU:1500  Metric:1
          RX packets:24 errors:0 dropped:0 overruns:0 frame:0
          TX packets:38 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0
          RX bytes:1608 (1.6 KB)  TX bytes:5800 (5.8 KB)

eno16777736 Link encap:Ethernet  HWaddr 00:0c:29:02:b9:13
          inet addr:192.168.218.129  Bcast:192.168.218.255  Mask:255.255.255.0
          inet6 addr: fe80::20c:29ff:fe02:b913/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:4934 errors:0 dropped:0 overruns:0 frame:0
          TX packets:4544 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000
          RX bytes:2909561 (2.9 MB)  TX bytes:577079 (577.0 KB)

lo        Link encap:Local Loopback
          inet addr:127.0.0.1  Mask:255.0.0.0
          inet6 addr: ::1/128 Scope:Host
          UP LOOPBACK RUNNING  MTU:65536  Metric:1
          RX packets:1416 errors:0 dropped:0 overruns:0 frame:0
          TX packets:1416 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0
          RX bytes:128893 (128.8 KB)  TX bytes:128893 (128.8 KB)

$ docker ps -q | xargs docker inspect --format '{{ .Id }}: NetworkMode={{ .HostConfig.NetworkMode }}'
52afb14d08b9271bd96045bebd508325a2adff98dbef8c10c63294989441954d: NetworkMode=host
While auditing it should be checked that all the containers by default should have network mode set to default and not host.

$ docker ps -q | xargs docker inspect --format '{{ .Id }}: NetworkMode={{ .HostConfig.NetworkMode }}'
1aca7fe47882da0952702c383815fc650f24da2c94029b5ad8af165239b78968: NetworkMode=default
Bind incoming container traffic to a specific host interface

If you have multiple network interfaces on your host machine, the container can accept connections on the exposed ports on any network interface. This might not be desired and may not be secured. Many a times a particular interface is exposed externally and services such as intrusion detection, intrusion prevention, firewall, load balancing, etc. are run on those interfaces to screen incoming public traffic. Hence, you should not accept incoming connections on any interface. You should only allow incoming connections from a particular external interface.

As shown below the machine has two network interfaces and by default if we run a nginx container it will get binded to localhost (0.0.0.0) that means this container will be accessible from both the IP address which can result in intrusion attack if any of them are not monitored.

$ ifconfig
docker0   Link encap:Ethernet  HWaddr 02:42:3f:3c:d7:3c
          inet addr:172.17.0.1  Bcast:0.0.0.0  Mask:255.255.0.0
          UP BROADCAST MULTICAST  MTU:1500  Metric:1
          RX packets:0 errors:0 dropped:0 overruns:0 frame:0
          TX packets:0 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0
          RX bytes:0 (0.0 B)  TX bytes:0 (0.0 B)

eno16777736 Link encap:Ethernet  HWaddr 00:0c:29:02:b9:13
          inet addr:192.168.218.129  Bcast:192.168.218.255  Mask:255.255.255.0
          inet6 addr: fe80::20c:29ff:fe02:b913/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:259 errors:0 dropped:0 overruns:0 frame:0
          TX packets:242 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000
          RX bytes:148095 (148.0 KB)  TX bytes:27195 (27.1 KB)

eno33554992 Link encap:Ethernet  HWaddr 00:0c:29:02:b9:1d
          inet addr:192.168.218.130  Bcast:192.168.218.255  Mask:255.255.255.0
          inet6 addr: fe80::20c:29ff:fe02:b91d/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:45 errors:0 dropped:0 overruns:0 frame:0
          TX packets:53 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000
          RX bytes:5931 (5.9 KB)  TX bytes:8452 (8.4 KB)

$ docker run -d -p 4915:80 nginx
26acfc7851a75c71c1315ee272d35ea56ea724842617074f4bd3a0026b5e4261

$ docker port 26ac
80/tcp -> 0.0.0.0:4915
In order to restrict this we should bind container to one of the IP address using the “-p” flag;

$ docker run -d -p 192.168.218.129:4915:80 nginx
f191f3aaf9052803a46dce1d65e2bf6f44e2c5cc929a713c40931b4a0d871d7e

$ docker ps -q
f191f3aaf905

$ docker port f191
80/tcp -> 192.168.218.129:4915
Do not share the host’s process namespace

PID namespace provides separation of processes. The PID Namespace removes the view of the system processes, and allows process ids to be reused including PID 1. If the host’s PID namespace is shared with the container, it would basically allow processes within the container to see all of the processes on the host system. This breaks the benefit of process level isolation between the host and the containers. Someone having access to the container can eventually know all the processes running on the host system and can even kill the host system processes from within the container. This can be catastrophic. Hence, do not share the host’s process namespace with the containers.

In this section we can see that if the container gets the pid of the host then it actually can access all the system level process of the host and can kill them as well causing potential threat. So, thus while auditing it should be checked that PID Mode should not be set to host for all the containers.

docker run -it --pid=host ubuntu /bin/bash
$ ps -ef
UID         PID   PPID  C STIME TTY          TIME CMD
root          1      0  0 12:26 ?        00:00:03 /sbin/init auto noprompt
root          2      0  0 12:26 ?        00:00:00 [kthreadd]
root          3      2  0 12:26 ?        00:00:00 [ksoftirqd/0]
root          5      2  0 12:26 ?        00:00:00 [kworker/0:0H]
root          7      2  0 12:26 ?        00:00:01 [rcu_sched]
root          8      2  0 12:26 ?        00:00:00 [rcu_bh]

$ docker ps -q | xargs docker inspect --format '{{ .Id }}: PidMode={{ .HostConfig.PidMode }}'
e42faa09133dd717d50da59af516dd3410db3889ffb9ef2767438b24a7b96a74: PidMode=host
Do not mount sensitive host system directories on containers

If sensitive directories are mounted in read-write mode, it would be possible to make changes to files within those sensitive directories. The changes might bring down security implications or unwarranted changes that could put the Docker host in compromised state.

If /run/systemd, sensitive directory is mounted in the container then we can actually shutdown the host from the container itself.

$ docker run -ti -v /run/systemd:/run/systemd centos /bin/bash
[root@1aca7fe47882 /]# systemctl status docker
docker.service - Docker Application Container Engine
   Loaded: loaded (/lib/systemd/system/docker.service; enabled)
   Active: active (running) since Sun 2015-11-29 12:22:50 UTC; 21min ago
     Docs: https://docs.docker.com
 Main PID: 758
   CGroup: /system.slice/docker.service

[root@1aca7fe47882 /]# shutdown
It can be audited by using the command below which returns the list of current mapped directories and whether they are mounted in read-write mode for each container instance;

$ docker ps -q | xargs docker inspect --format '{{ .Id }}: Volumes={{ .Volumes }} VolumesRW={{ .VolumesRW }}'


Container Images and Build file

Container base images and build files govern the fundamentals of how a container instance from a particular image would behave. Ensuring that you are using proper base images and appropriate build files can be very important for building your containerized infrastructure. Below are some of the recommendations that you should follow for container base images and build files to ensure that your containerized infrastructure is secure.

Create a user for the container

Currently, mapping the container’s root user to a non-root user on the host is not supported by Docker. The support for user namespace would be provided in future releases. This creates a serious user isolation issue. It is thus highly recommended to ensure that there is a non-root user created for the container and the container is run using that user.

As we can see below that by default Centos docker image has user field as blank that means by default container will get root user during runtime which should be avoided.

$ docker inspect centos
[
{
    "Id": "e9fa5d3a0d0e19519e66af2dd8ad6903a7288de0e995b6eafbcb38aebf2b606d",
    "RepoTags": [
        "centos:latest"
    ],
    "RepoDigests": [],
    "Parent": "c9853740aa059d078b868c4a91a069a0975fb2652e94cc1e237ef9b961afa572",
    "Comment": "",
    "Created": "2015-10-13T23:29:04.138328589Z",
    "Container": "eaa200e2e187340f0707085b9b4eab5658b13fd190af68c71a60f6283578172f",
    "ContainerConfig": {
        "Hostname": "7aa5783a47d5",
        "Domainname": "",
        "User": "",
        "AttachStdin": false,
        "AttachStdout": false,
        "AttachStderr": false,
        "Tty": false,
        "OpenStdin": false,
        "StdinOnce": false,
        "Env": null,
        "Cmd": [
            "/bin/sh",
            "-c",
            "#(nop) CMD [\"/bin/bash\"]"
        ],
        "Image": "4234bfdd88f8ed2bc4607bd2ebba2d41d61e2693ad0d184e7b05e1b57f8b8b33",
        "Volumes": null,
        "WorkingDir": "",
        "Entrypoint": null,
        "OnBuild": null,
        "Labels": {
            "License": "GPLv2",
            "Vendor": "CentOS"
        }
    },
    "DockerVersion": "1.8.2",
    "Author": "The CentOS Project \u003ccloud-ops@centos.org\u003e",
    "Config": {
        "Hostname": "7aa5783a47d5",
        "Domainname": "",
        "User": "",
        "AttachStdin": false,
        "AttachStdout": false,
        "AttachStderr": false,
                "Tty": false,
        "OpenStdin": false,
        "StdinOnce": false,
        "Env": null,
        "Cmd": [
            "/bin/bash"
        ],
        "Image": "4234bfdd88f8ed2bc4607bd2ebba2d41d61e2693ad0d184e7b05e1b57f8b8b33",
        "Volumes": null,
        "WorkingDir": "",
        "Entrypoint": null,
        "OnBuild": null,
        "Labels": {
            "License": "GPLv2",
            "Vendor": "CentOS"
        }
    },
    "Architecture": "amd64",
    "Os": "linux",
    "Size": 0,
    "VirtualSize": 172289754,
    "GraphDriver": {
        "Name": "aufs",
        "Data": null
    }
}
]
While building the docker image we can provide the “test” user the less-privileged user in the Dockerfile as shown below;

$ cd
$ mkdir test-container
$ cd test-container/
$ cat Dockerfile
FROM centos:latest
RUN useradd test
USER test

root@ubuntu:~/test-container# docker build -t vkohli .
Sending build context to Docker daemon 2.048 kB
Step 1 : FROM centos:latest
 ---> e9fa5d3a0d0e
Step 2 : RUN useradd test
 ---> Running in 0c726d186658
 ---> 12041ebdfd3f
Removing intermediate container 0c726d186658
Step 3 : USER test
 ---> Running in 86c5e0599c72
 ---> af4ba8a0fec5
Removing intermediate container 86c5e0599c72
Successfully built af4ba8a0fec5

$ docker images | grep vkohli
vkohli              latest              af4ba8a0fec5        9 seconds ago       172.6 MB
When we start the docker container we can see that it gets “test” user and docker inspect command also shows the default user as “test”;

$ docker run -it vkohli /bin/bash
[test@2ff11ee54c5f /]$ whoami
test
[test@2ff11ee54c5f /]$ exit

$ docker inspect vkohli
[
{
    "Id": "af4ba8a0fec558d68b4873e2a1a6d8a5ca05797e0bfbab0772bcedced15683ea",
    "RepoTags": [
        "vkohli:latest"
    ],
    "RepoDigests": [],
    "Parent": "12041ebdfd3f38df3397a8961f82c225bddc56588e348761d3e252eec868d129",
    "Comment": "",
    "Created": "2015-11-27T14:10:49.206969614Z",
    "Container": "86c5e0599c72285983f3c5511fdec940f70cde171f1bfb53fab08854fe6d7b12",
    "ContainerConfig": {
        "Hostname": "7aa5783a47d5",
        "Domainname": "",
        "User": "test",
        "AttachStdin": false,
        "AttachStdout": false,
        "AttachStderr": false,
        "Tty": false,
        "OpenStdin": false,
        "StdinOnce": false,
        "Env": [
            "PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
        ],
        "Cmd": [
            "/bin/sh",
            "-c",
            "#(nop) USER [test]"
        ],
        "Image": "12041ebdfd3f38df3397a8961f82c225bddc56588e348761d3e252eec868d129",
        "Volumes": null,
        "WorkingDir": "",
        "Entrypoint": null,
        "OnBuild": [],
        "Labels": {
            "License": "GPLv2",
            "Vendor": "CentOS"
        }
    },
    "DockerVersion": "1.9.1",
    "Author": "",
    "Config": {
        "Hostname": "7aa5783a47d5",
        "Domainname": "",
        "User": "test",
        "AttachStdin": false,
        "AttachStdout": false,
        "AttachStderr": false,
        "Tty": false,
        "OpenStdin": false,
        "StdinOnce": false,
        "Env": [
            "PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
        ],
        "Cmd": [
            "/bin/bash"
        ],
        "Image": "12041ebdfd3f38df3397a8961f82c225bddc56588e348761d3e252eec868d129",
        "Volumes": null,
        "WorkingDir": "",
        "Entrypoint": null,
        "OnBuild": [],
        "Labels": {
            "License": "GPLv2",
            "Vendor": "CentOS"
        }
    },
    "Architecture": "amd64",
    "Os": "linux",
    "Size": 0,
    "VirtualSize": 172585404,
    "GraphDriver": {
        "Name": "aufs",
        "Data": null
    }
}
]




Docker Security Operations

This sections covers some of the operational security aspects for Docker deployments. These are best practices that should be followed. Most of the recommendations here are just reminders that organizations should extend their current security best practices and policies to include containers.

Avoid Container Sprawl

The flexibility of containers makes it easy to run multiple instances of applications and indirectly leads to Docker images that exist at varying security patch levels. It also means that you are consuming host resources that otherwise could have been used for running ‘useful’ containers. Having more than just the manageable number of containers on a particular host makes the situation vulnerable to mishandling, misconfiguration and fragmentation. Thus, avoid container sprawl and keep the number of containers on a host to a manageable total.

$ docker info
Containers: 5
Images: 21
Server Version: 1.9.1
Storage Driver: aufs
 Root Dir: /var/lib/docker/aufs
 Backing Filesystem: extfs
 Dirs: 31
 Dirperm1 Supported: true
Execution Driver: native-0.2
Logging Driver: json-file
Kernel Version: 4.2.0-16-generic
Operating System: Ubuntu 15.10
CPUs: 1
Total Memory: 975.4 MiB
Name: ubuntu
ID: WLYI:SQ6A:OHOM:MBQJ:W67Z:JRQS:ZW4A:QSTI:7MWR:P5H7:PYTM:GG3S
WARNING: No swap limit support

$ docker ps
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
As we can see above “5” containers can be seen in the docker info command but actually there are no running containers, the rest containers can be listed as shown below which are not in running state but occuping space on the host and can cause container sprawl.

$ docker ps -a
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS                           PORTS                           NAMES
08c82f15168a        centos              "bash"                   About an hour ago   Exited (127) About an hour ago                                   awesome_hamilton
34e34a535497        nginx               "nginx -g 'daemon off"   About an hour ago   Exited (137) About an hour ago   443/tcp, 0.0.0.0:4915->80/tcp   drunk_franklin
df006460c9d1        centos              "bash"                   3 hours ago         Exited (0) 3 hours ago                                           amazing_goldstine
39fc070bf79d        nginx               "nginx -g 'daemon off"   3 hours ago         Exited (0) About an hour ago                                     stupefied_mccarthy
30184533bb3c        hello-world         "/hello"                 5 hours ago         Exited (0) 5 hours ago                                           furious_joliot
It is always advisable to run the docker container with “rm” option so that when you exit the container it gets removed from the host as well, shown below we can see that container after the exit is not listed in “docker ps -a” option;

$ docker run --rm=true -it vkohli
[test@411323c15f38 /]$ ls
bin  etc   lib    lost+found  mnt  proc  run   srv  tmp  var
dev  home  lib64  media       opt  root  sbin  sys  usr
[test@411323c15f38 /]$ exit
exit

$ docker ps -a
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS                           PORTS                           NAMES
08c82f15168a        centos              "bash"                   About an hour ago   Exited (127) About an hour ago                                   awesome_hamilton
34e34a535497        nginx               "nginx -g 'daemon off"   About an hour ago   Exited (137) About an hour ago   443/tcp, 0.0.0.0:4915->80/tcp   drunk_franklin
df006460c9d1        centos              "bash"                   3 hours ago         Exited (0) 3 hours ago                                           amazing_goldstine
39fc070bf79d        nginx               "nginx -g 'daemon off"   3 hours ago         Exited (0) About an hour ago                                     stupefied_mccarthy
30184533bb3c        hello-world         "/hello"                 5 hours ago         Exited (0) 5 hours ago                                           furious_joliot
In order to remove all the non-running containers from the host following command can be used;

$ docker rm `docker ps --no-trunc -aq`

