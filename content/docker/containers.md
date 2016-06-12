title: Docker Containers
date: 2016-05-02
description: A tutorial on Docker
tags: docker, kubernets, spark, programming, hadoop, bigdata, yarn

Docker Link Flag

In order to connect together multiple docker containers or services running inside docker container, ‘–link’ flag can be used in order to securely connect and provide a channel to transfer information from one container to another. The below example shows a simple application of using a Wordpress container linked to MySQL container.

Pull the latest MySql container

$ docker pull mysql:latest
latest: Pulling from mysql
..........................
Run MySql Container in detach mode

$ docker run --name mysql-container -e MYSQL_ROOT_PASSWORD=wordpress -d mysql
89c8554d736862ad5dbb8de5a16e338069ba46f3d7bbda9b8bf491813c842532
We will be running this database container with name “mysql-wordpress” and will set root password for MySQL container.

Pull Wordpress docker container

In the new terminal, pull the official wordpress container

$ docker pull wordpress:latest
latest: Pulling from wordpress
..............................
Run the wordpress container linking it to MySQL Container

$ docker run -e WORDPRESS_DB_PASSWORD=password --name wordpress-container --link mysql-container:mysql -p 8080:80 -d wordpress
189c0f04ce7694b4f9fadd36624f6f818023d8d1f3ed1c56de5a516255f328a9
As, we have linked both the container now wordpress container can be accessed from browser using the address http://localhost:8080 and setup of wordpress can be done easily.



Docker Compose

We will run the same previous application of wordpress and MySQL linking in this tutorial but with Docker compose which was launched recently and is a tool use to define and run complex linked applications with docker. With docker compose we can define the entire multi-container application in single file and then the application can be spinned up using one command.

Create a new project folder

$ mkdir dockercompose
$ cd dockercompose
Create Docker compose file

Create docker-compose.yml with preferred editor having the following contents

web:
    image: wordpress
    links:
     - mysql
    environment:
     - WORDPRESS_DB_PASSWORD=sample
    ports:
     - "127.0.0.3:8080:80"
mysql:
image: mysql:latest
environment:
 - MYSQL_ROOT_PASSWORD=sample
 - MYSQL_DATABASE=wordpress
Get the linked containers up

$ docker-compose up
Creating dockercompose_mysql...
Creating dockercompose_web...
Attaching to dockercompose_mysql, dockercompose_web
mysql | Initializing database
..............
Visit the IP address http://127.0.0.3:8080 in order to see the setup page of the newly created linked wordpress container.


