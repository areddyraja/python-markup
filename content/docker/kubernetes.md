title: Docker with Kubernetes
date: 2016-05-02
description: A tutorial on Docker
tags: docker, kubernets, spark, programming, hadoop, bigdata, yarn

Getting Started

Installation

Ubuntu

Switch to root user
$ sudo -s
[sudo] password for your_user:
Install pre-requisite software packages
$ apt-get update
$ apt-get install ssh
$ apt-get install docker.io
$ apt-get install curl
Password-less ssh login setup, accept all the default parameters in the prompt of the below command (required for Kubernetes installation)
$ ssh-keygen -t rsa
Generating public/private rsa key pair.
Enter file in which to save the key (/root/.ssh/id_rsa):
Enter passphrase (empty for no passphrase):
Enter same passphrase again:
Your identification has been saved in /root/.ssh/id_rsa.
Your public key has been saved in /root/.ssh/id_rsa.pub.
The key fingerprint is:
e1:c9:a5:dd:80:ee:cd:f0:c8:11:6c:a5:d4:ba:ff:cc root@vkohli-Latitude-E7440
The key's randomart image is:
+--[ RSA 2048]----+
|          ...    |
|         + o.    |
|        o B.     |
|       + B..+    |
|        S o..    |
|       . *..     |
|        . *.     |
|         .  .o   |
|             .E  |
+-----------------+
Copy the ssh id_rsa key locally
$ ssh-copy-id -i /root/.ssh/id_rsa.pub 127.0.0.1
In case this command fails please use this alternative solution in order to add the key

$ cat /root/.ssh/id_rsa.pub >> /root/.ssh/authorized_keys
Validate the password-less ssh-login
$ ssh root@127.0.0.1
root@vkohli-virtual-machine:~$ exit
logout
Connection to 127.0.0.1 closed
Get the Kubernetes release bundle from the official github repository
$ wget https://github.com/GoogleCloudPlatform/kubernetes/releases/download/v1.0.1/kubernetes.tar.gz
Untar the Kubernetes bundle in the same directory
$ tar -xvf kubernetes.tar.gz
We will build the binaries of Kubernetes code specifically for ubuntu cluster
$ cd kubernetes/cluster/ubuntu
Execute the following shell script

$ ./build.sh
Download flannel release ...
Flannel version is 0.4.0
% Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                Dload  Upload   Total   Spent    Left  Speed
100   411    0   411    0     0    252      0 --:--:--  0:00:01 --:--:--   252
100 2393k  100 2393k    0     0   204k      0  0:00:11  0:00:11 --:--:--  388k
Download etcd release ...
% Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   410    0   410    0     0    272      0 --:--:--  0:00:01 --:--:--   272
100 3713k  100 3713k    0     0   286k      0  0:00:12  0:00:12 --:--:--  496k
Download kubernetes release ...
% Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                Dload  Upload   Total   Spent    Left  Speed
100   396    0   396    0     0    279      0 --:--:--  0:00:01 --:--:--   279
100 97.8M  100 97.8M    0     0   715k      0  0:02:20  0:02:20 --:--:--  501k
~/kubernetes/cluster/ubuntu/kubernetes/server ~/kubernetes/cluster/ubuntu
~/kubernetes/cluster/ubuntu
Done! All your commands locate in ./binaries dir
This shell script will download and build the latest version of K8s, etcd and flannel binaries which can be found at following location;

$ cd binaries
$ ls
kubectl  master  minion
kubectl binary controls the Kubernetes cluster manager and the folder master & minion contains the binaries built for the purpose of configuring K8s master and node respectively.

Configure the cluster information by editing only the following parameters of the file cluster/ubuntu/config-default.sh in the editor of your choice.
$ cd
$ vi kubernetes/cluster/ubuntu/config-default.sh
export nodes="root@127.0.0.1"
export roles="ai"
export NUM_MINIONS=${NUM_MINIONS:-1}
Only update the above mentioned information in the file, rest of the configuration will remain as it is. The first variable nodes defines all the cluster nodes, in our case same machine will be configured as master and node so it contains only one entry.The role below “ai” specifies that same machine will act as master, “a” stands for master and “i” stands for node.

Now, we will be starting the cluster with the following command;
$ cd kubernetes/cluster
$ KUBERNETES_PROVIDER=ubuntu ./kube-up.sh
Starting cluster using provider: ubuntu
... calling verify-prereqs
... calling kube-up
FLANNEL_NET
172.16.0.0/16
Deploying master and minion on machine 127.0.0.1

config-default.sh                                                                                100% 2904     2.8KB/s   00:00
util.sh                                                                                          100%   13KB  13.4KB/s   00:00
flanneld.conf                                                                                    100%  569     0.6KB/s   00:00
kube-controller-manager.conf                                                                     100%  746     0.7KB/s   00:00
kube-apiserver.conf                                                                              100%  676     0.7KB/s   00:00
etcd.conf                                                                                        100%  576     0.6KB/s   00:00
kube-scheduler.conf                                                                              100%  676     0.7KB/s   00:00
kube-apiserver                                                                                   100% 2358     2.3KB/s   00:00
kube-controller-manager                                                                          100% 2672     2.6KB/s   00:00
etcd                                                                                             100% 2073     2.0KB/s   00:00
flanneld                                                                                         100% 2159     2.1KB/s   00:00
kube-scheduler                                                                                   100% 2360     2.3KB/s   00:00
reconfDocker.sh                                                                                  100% 1493     1.5KB/s   00:00
kube-proxy.conf                                                                                  100%  648     0.6KB/s   00:00
flanneld.conf                                                                                    100%  569     0.6KB/s   00:00
kubelet.conf                                                                                     100%  634     0.6KB/s   00:00
etcd.conf                                                                                        100%  576     0.6KB/s   00:00
kube-proxy                                                                                       100% 2230     2.2KB/s   00:00
etcd                                                                                             100% 2073     2.0KB/s   00:00
flanneld                                                                                         100% 2159     2.1KB/s   00:00
kubelet                                                                                          100% 2162     2.1KB/s   00:00
kube-apiserver                                                                                   100%   34MB  33.7MB/s   00:00
kube-controller-manager                                                                          100%   26MB  26.2MB/s   00:00
etcdctl                                                                                          100% 6041KB   5.9MB/s   00:00
etcd                                                                                             100% 6494KB   6.3MB/s   00:00
flanneld                                                                                         100% 8695KB   8.5MB/s   00:00
kube-scheduler                                                                                   100%   17MB  17.0MB/s   00:00
kube-proxy                                                                                       100%   17MB  16.8MB/s   00:00
etcdctl                                                                                          100% 6041KB   5.9MB/s   00:00
etcd                                                                                             100% 6494KB   6.3MB/s   00:00
flanneld                                                                                         100% 8695KB   8.5MB/s   00:00
kubelet                                                                                          100%   33MB  33.2MB/s   00:01
[sudo] password to copy files and start node:
etcd start/running, process 1125
Connection to 127.0.0.1 closed.
Validating master
Validating root@127.0.0.1

Kubernetes cluster is running.  The master is running at:

  http://127.0.0.1

FLANNEL_NET
172.16.0.0/16
Using master 127.0.0.1
Wrote config for ubuntu to /home/root/.kube/config
... calling validate-cluster

Waiting for 1 ready nodes. 0 ready nodes, 0 registered. Retrying.
Found 1 nodes.
        NAME        LABELS                             STATUS
1       127.0.0.1   kubernetes.io/hostname=127.0.0.1   Ready
Validate output:
NAME                 STATUS    MESSAGE   ERROR
scheduler            Healthy   ok        nil
etcd-0               Healthy   {"action":"get","node":{"dir":true,"nodes":[{"key":"/registry","dir":true,"modifiedIndex":3,"createdIndex":3},{"key":"/coreos.com","dir":true,"modifiedIndex":16,"createdIndex":16}]}}
                     nil
controller-manager   Healthy   ok        nil
Cluster validation succeeded
Done, listing cluster services:

Kubernetes master is running at http://127.0.0.1:8080
Basic Commands with example

Info command

We will add kubectl binary to path in order to manage the Kubernetes cluster.

$ export PATH=$PATH:~/kubernetes/cluster/ubuntu/binaries
$ kubectl --help
kubectl controls the Kubernetes cluster manager.

Find more information at https://github.com/GoogleCloudPlatform/kubernetes.

Usage:
  kubectl [flags]
  kubectl [command]

Available Commands:
  get            Display one or many resources
  describe       Show details of a specific resource
  create         Create a resource by filename or stdin
  update         Update a resource by filename or stdin.
  delete         Delete a resource by filename, stdin, resource and ID, or by resources and label selector.
  namespace      SUPERCEDED: Set and view the current Kubernetes namespace
  logs           Print the logs for a container in a pod.
  rolling-update Perform a rolling update of the given ReplicationController.
  scale          Set a new size for a Replication Controller.
  exec           Execute a command in a container.
  port-forward   Forward one or more local ports to a pod.
  proxy          Run a proxy to the Kubernetes API server
  run            Run a particular image on the cluster.
  stop           Gracefully shut down a resource by id or filename.
  expose         Take a replicated application and expose it as Kubernetes Service
  label          Update the labels on a resource
  config         config modifies kubeconfig files
  cluster-info   Display cluster info
  api-versions   Print available API versions.
  version        Print the client and server version information.
  help           Help about any command

Flags:
      --alsologtostderr=false: log to standard error as well as files
      --api-version="": The API version to use when talking to the server
      --certificate-authority="": Path to a cert. file for the certificate authority.
      --client-certificate="": Path to a client key file for TLS.
      --client-key="": Path to a client key file for TLS.
      --cluster="": The name of the kubeconfig cluster to use
      --context="": The name of the kubeconfig context to use
  -h, --help=false: help for kubectl
      --insecure-skip-tls-verify=false: If true, the server's certificate will not be checked for validity. This will make your HTTPS connections insecure.
      --kubeconfig="": Path to the kubeconfig file to use for CLI requests.
      --log-backtrace-at=:0: when logging hits line file:N, emit a stack trace
      --log-dir=: If non-empty, write log files in this directory
      --log-flush-frequency=5s: Maximum number of seconds between log flushes
      --logtostderr=true: log to standard error instead of files
      --match-server-version=false: Require server version to match client version
      --namespace="": If present, the namespace scope for this CLI request.
      --password="": Password for basic authentication to the API server.
  -s, --server="": The address and port of the Kubernetes API server
      --stderrthreshold=2: logs at or above this threshold go to stderr
      --token="": Bearer token for authentication to the API server.
      --user="": The name of the kubeconfig user to use
      --username="": Username for basic authentication to the API server.
      --v=0: log level for V logs
      --validate=false: If true, use a schema to validate the input before sending it
      --vmodule=: comma-separated list of pattern=N settings for file-filtered logging


Use "kubectl help [command]" for more information about a command.
Now, we will validate if the K8s cluster created above is properly configured;

$ kubectl get nodes
NAME        LABELS                             STATUS
127.0.0.1   kubernetes.io/hostname=127.0.0.1   Ready
The Kubernetes UI can be accessed at the following address https://127.0.0.1/ui . Suppose in case it is not accessible please run the following services and try again.

$ kubectl create -f addons/kube-ui/kube-ui-rc.yaml --namespace=kube-system
$ kubectl create -f addons/kube-ui/kube-ui-svc.yaml --namespace=kube-system
Create a Wordpress pod example

The below mentioned command will create a wordpress container which runs at port 80 and then expose it on the host port 81. The image ‘tutum/wordpress’ is fetched from the docker hub. By default this command will take the replication controller value as “1”.

$ kubectl run wordpress --image=tutum/wordpress --port=80 --hostport=81
CONTROLLER   CONTAINER(S)   IMAGE(S)          SELECTOR        REPLICAS
wordpress    wordpress      tutum/wordpress   run=wordpress   1
After some time wordpress container will be available to be accessed at the following address http://127.0.0.1:81, which can be used to setup personal blog. We can list the pod and its replication controller as follow;

$ kubectl get pods
NAME              READY     REASON    RESTARTS   AGE
wordpress-8fz7m   1/1       Running   0          3m
$ kubectl get rc
CONTROLLER   CONTAINER(S)   IMAGE(S)          SELECTOR        REPLICAS
wordpress    wordpress      tutum/wordpress   run=wordpress   1
Even the docker container at the node can be listed by using the following command;

$ docker ps
CONTAINER ID        IMAGE                                  COMMAND             CREATED             STATUS              PORTS                NAMES
e9e51db34a79        tutum/wordpress:latest                 "/run.sh"           10 minutes ago      Up 10 minutes                            k8s_wordpress.fad11ccd_wordpress-8fz7m_default_98ab2649-2e59-11e5-8972-ecf4bb2bbd90_e34544da
9992de964017        gcr.io/google_containers/pause:0.8.0   "/pause"            10 minutes ago      Up 10 minutes       0.0.0.0:81->80/tcp   k8s_POD.98d1e889_wordpress-8fz7m_default_98ab2649-2e59-11e5-8972-ecf4bb2bbd90_ab95514c
In order to delete a pod, we will have to delete the replication controller.

$ kubectl delete rc wordpress
replicationcontrollers/wordpress
Deleting the Kubernetes Cluster

Use the following command to delete the Kubernetes Cluster

$ KUBERNETES_PROVIDER=ubuntu ./kube-down.sh

Bringing down cluster using provider: ubuntu
FLANNEL_NET
172.16.0.0/16
Cleaning on node 127.0.0.1
The authenticity of host '127.0.0.1 (127.0.0.1)' can't be established.
ECDSA key fingerprint is ad:54:ab:4e:d0:3f:4c:32:e3:75:f7:ec:91:9e:29:6e.
Are you sure you want to continue connecting (yes/no)? yes
Warning: Permanently added '127.0.0.1' (ECDSA) to the list of known hosts.
ubuntu@127.0.0.1's password:
4405
[sudo] password for cleaning etcd data:
etcd stop/waiting
Connection to 127.0.0.1 closed.
Done




Kubernetes Example

Nginx Server Deployment using Kubernetes

Create a folder
$ mkdir nginx_kube_example
$ cd nginx_kube_example
Create the yaml file in the editor of your choice which will be used to deploy nginx pod
$ vi nginx_pod.yaml
apiVersion: v1
kind: ReplicationController
metadata:
  name: nginx
spec:
  replicas: 2
  selector:
    app: nginx
  template:
    metadata:
      name: nginx
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx
        ports:
        - containerPort: 80
Create the nginx pod using kubectl
$ kubectl create -f nginx_pod.yaml
In the above pod creation process, we have created two replicas of the nginx pod and its details can be listed as follow
$ kubectl get pods
NAME          READY     REASON    RESTARTS   AGE
nginx-karne   1/1       Running   0          14s
nginx-mo5ug   1/1       Running   0          14s
$ kubectl get rc
CONTROLLER   CONTAINER(S)   IMAGE(S)   SELECTOR    REPLICAS
nginx        nginx          nginx      app=nginx   2
$ docker ps
CONTAINER ID        IMAGE                                   COMMAND                CREATED             STATUS              PORTS               NAMES
1d3f9cedff1d        nginx:latest                            "nginx -g 'daemon of   41 seconds ago      Up 40 seconds                           k8s_nginx.6171169d_nginx-karne_default_5d5bc813-3166-11e5-8256-ecf4bb2bbd90_886ddf56
0b2b03b05a8d        nginx:latest                            "nginx -g 'daemon of   41 seconds ago      Up 40 seconds
Deploy the nginx service using yaml file in order to expose the nginx pod on the host port “82”
$ vi nginx_service.yaml
apiVersion: v1
kind: Service
metadata:
  labels:
    name: nginxservice
  name: nginxservice
spec:
  ports:
    # The port that this service should serve on.
    - port: 82
  # Label keys and values that must match in order to receive traffic for this service.
  selector:
    app: nginx
  type: LoadBalancer
Create the nginx service using kubectl
$kubectl create -f nginx_service.yaml
services/nginxservice
The nginx service can be listed as follow
$ kubectl get services
NAME           LABELS                                    SELECTOR    IP(S)          PORT(S)
kubernetes     component=apiserver,provider=kubernetes   <none>      192.168.3.1    443/TCP
nginxservice   name=nginxservice                         app=nginx   192.168.3.43   82/TCP
Now the nginx server test page can be accessed on the following URL; http://127.0.0.1:82

Now we will delete the nginx pod and service
$ kubectl delete service nginxservice
$ kubectl delete rc nginx
Pod Deployment with two containers

In the below example we will be running the two containers in same pod
$ vi nginx-mysql.json
{
   "id":"nginx-mysql",
   "kind": "Pod",
   "apiVersion": "v1",
   "metadata": {
      "name": "nginx-mysql",
      "labels": {
         "name": "nginx-mysql"
      }
   },
   "spec": {
      "containers": [
         {
            "name": "nginx",
            "image": "nginx",
            "ports": [
               {
                  "hostPort": 85,
                  "containerPort": 80
               }
            ]
         },
         {
            "name": "mysql",
            "image": "mysql",
            "ports": [
               {
                  "hostPort": 3306,
                  "containerPort": 3306
               }
            ]
         }
      ]
   }
}
Create the pod
$ kubectl create -f nginx-mysql.json
$ kubectl get pods


