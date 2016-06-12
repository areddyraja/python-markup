title: Docker MicroServices
date: 2016-05-02
description: A tutorial on Docker
tags: docker, kubernets, spark, programming, hadoop, bigdata, yarn

Dockerize Simple Flask App

In this tutorial you will learn how to create a simple Flask App and run it inside a docker container

Required Software

docker (1.6.0 or above)
python 2.7 or above
Linux VM - (We used ubuntu 14.04 64 bit)
Create the Flask App and Deployment files

Create a folder web. All our files will be inside this directory

Flask Application

Create a new file app.py inside web and add the following python code

From flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Flask Dockerized'

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
Requirements File

Requirements file states the software required to be installed in the container. Create a file requirements.txt inside web folder

Flask==0.10.1
Dockerfile

This file is needs to create a docker image and deploy it

FROM ubuntu:latest
MAINTAINER Rajdeep Dua "dua_rajdeep@yahoo.com"
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["app.py"]
Build the docker Image

Run the following command to build the docker image flask-sample-one from web directory

$ docker build -t flask-sample-one:latest .
Run the Docker Container

$ docker run -d -p 5000:5000 flask-sample-one
You can find the container runtime details as shown below

$ docker ps -a
CONTAINER ID        IMAGE                              COMMAND                CREATED             STATUS                             PORTS                    NAMES
92fb4d65c7cd        flask-sample-one:latest            "python app.py"        22 minutes ago      Up 22 minutes                      0.0.0.0:5000->5000/tcp   clever_blackwell




Run Simple Flask App using Docker Compose

In this tutorial you will learn how to create a simple Flask App and run it inside a docker container using docker Compose

Required Software

docker (1.6.0 or above)
docker-compose (1.3.1+)
python 2.7 or above
Linux VM - (We used ubuntu 14.04 64 bit)
Create the Flask App and Deployment files

Create a parent directory flask_compose_sample

$ mkdir flask_compose_sample
$ cd flask_compose_sample
Create a folder web. All our files for the flask app will be inside this directory.

$ mkdir web
$ cd web
Flask Application

Create a new file app.py inside web and add the following python code

From flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Flask Dockerized'

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
Requirements File

Requirements file states the software required to be installed in the container. Create a file requirements.txt inside web folder

Flask==0.10.1
Dockerfile

This file is needed to create a docker image and deploy it

FROM ubuntu:latest
MAINTAINER Rajdeep Dua "dua_rajdeep@yahoo.com"
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["app.py"]
Docker Compose File

Go to the parent directory flask_compose_sample and create a file docker-compose.yml. For each service there is a parent tag and child tags which specify

web

Builds from the Dockerfile in the current directory.
Forwards the exposed port 5000 on the container to port 5000 on the host machine..
Mounts the current directory on the host to /code inside the container allowing you to modify the code without having to rebuild the image.
web:
  build: ./web
  ports:
   - "5000:5000"
  volumes:
   - .:/code
Build and Run the Service using Docker Compose

Run the following command to build the docker image flask-sample-one from web directory and deploy is as a service

$ docker-compose up
You can go to the browser and open the url http://localhost:5000 to see the HTML rendered

../_images/flask_simple_app.png
You can find the container runtime details as shown below

$ docker ps -a
CONTAINER ID        IMAGE                              COMMAND                CREATED             STATUS                        PORTS                    NAMES
06351e6fa146 flaskcomposesample_web:latest “python app.py” 38 minutes ago Up 38 minutes 0.0.0.0:5000->5000/tcp flaskcomposesample_web_1 0.0.0.0:5000->5000/tcp clever_blackwell


Run Flask App with MongoDB using Docker Compose

In this tutorial you will learn how to create a simple Flask App with MongoDB integration, deploy and run it inside a docker container using docker Compose

Required Software

docker (1.6.0 or above)
docker-compose (1.3.1+)
python 2.7 or above
Linux VM - (We used ubuntu 14.04 64 bit)
Files to be created in the app

├── app.py
├── docker-compose.yml
├── Dockerfile
├── README.md
├── requirements.txt
└── templates
    └── todo.html
Create the Parent Directory

Create a parent directory flask_mongo_compose_sample

$ mkdir flask_compose_sample
$ cd flask_compose_sample
Flask Application

Create a new file app.py and add the following python code

import os
from flask import Flask, redirect, url_for, request, render_template
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient(
    os.environ['DB_PORT_27017_TCP_ADDR'],
    27017)
db = client.tododb


@app.route('/')
def todo():

    _items = db.tododb.find()
    items = [item for item in _items]

    return render_template('todo.html', items=items)


@app.route('/new', methods=['POST'])
def new():

    item_doc = {
        'name': request.form['name'],
        'description': request.form['description']
    }
    db.tododb.insert_one(item_doc)

    return redirect(url_for('todo'))

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
Template file

This file todo.html contains the Jinja template to display HTML. These will be stored in templates folder

<form action="/new" method="POST">
  <input type="text" name="name"></input>
  <input type="text" name="description"></input>
  <input type="submit"></input>
</form>

{% for item in items %}
  <h1> {{ item.name }} </h1>
  <p> {{ item.description }} <p>
{% endfor %}
Requirements File

Requirements file states the software required to be installed in the container. Create a file requirements.txt inside web folder

flask
pymongo
Dockerfile

This file is needed to create a docker image and deploy it

FROM python:2.7
ADD . /todo
WORKDIR /todo
RUN pip install -r requirements.txt
Docker Compose File

Go to the parent directory flask_mongo_compose_sample and create a file docker-compose.yml. For each service there is a parent tag and child tags which specify

web

Builds from the Dockerfile in the current directory.
Forwards the exposed port 5000 on the container to port 5000 on the host machine..
Mounts the current directory on the host to /todo inside the container allowing you to modify the code without having to rebuild the image.
Links to the container name db which is the MongoDB container
db

Creates a standard MongoDB container from the image mongo:3.0.2

web:
  build: .
  command: python -u app.py
  ports:
    - "5000:5000"
  volumes:
    - .:/todo
  links:
    - db
db:
  image: mongo:3.0.2
Build and Run the Service using Docker Compose

Run the following command to build the docker image flask_mongo_compose_sample from web directory and deploy is as a service

$ docker-compose build
$ docker-compose up
You can go to the browser and open the url http://localhost:5000 to see the HTML rendered


Building Docker-Compose based MicroServices for a Flask Application

In this tutorial you will learn how to run a Flask Based Application with nginx as a microservice using Docker and Docker Compose.

Setup

Please install the following components before starting the lab

docker (1.6.0 or above)
docker-compose (1.3.1) or above
Test out the installs:

$ docker --version
Docker version 1.6.2, build 7c8fca2
$ docker-compose --version
docker-compose 1.3.1
Clone the Project

Next clone the project from the repo or create your own project based on the project structure found on the repo:

├── docker-compose.yml
├── nginx
│   ├── Dockerfile
│   └── sites-enabled
│       └── flask_project
└── web
    ├── Dockerfile
    ├── app.py
    ├── config.py
    ├── create_db.py
    ├── models.py
    ├── requirements.txt
    ├── static
    │   ├── css
    │   │   ├── bootstrap.min.css
    │   │   └── main.css
    │   ├── img
    │   └── js
    │       ├── bootstrap.min.js
    │       └── main.js
    └── templates
        ├── _base.html
        └── index.html
Docker Compose

Four Services are defined – web, nginx, postgres, and data.

../_images/nginx_flask_postgres_diagram1.png
web : The web service is built using the instructions in the Dockerfile within the “web” directory – where the Python environment is setup, requirements are installed, and the Flask app is fired up on port 8000. That port is then forwarded to port 80 on the host environment. This service also adds environment variables to the container that are defined in the .env file.
nginx : The nginx service is used for reverse proxy to forward requests either to the Flask app or the static files. It refers to the volumne of the web service
postgres : The postgres service is built from the the official PostgreSQL image from Docker Hub, which install Postgres and runs the server on the default port 5432.
data : There is a separate volume container that’s used to store the database data. This helps ensure that the data persists even if the Postgres container is completely destroyed.
Refer to the docker-compose.yml file:

web:
  restart: always
  build: ./web
  expose:
    - "8000"
  links:
    - postgres:postgres
  volumes:
    - /usr/src/app/static
  env_file: .env
  command: /usr/local/bin/gunicorn -w 2 -b :8000 app:app

nginx:
  restart: always
  build: ./nginx/
  ports:
    - "80:80"
  volumes:
    - /www/static
  volumes_from:
    - web
  links:
    - web:web

data:
  restart: always
  image: postgres:latest
  volumes:
    - /var/lib/postgresql
  command: true

postgres:
  restart: always
  image: postgres:latest
  volumes_from:
    - data
  ports:
    - "5432:5432"
Build Images

Now, to get the containers running, build the images and then start the services:

$ docker-compose build
Start all the containers

$ docker-compose up -d
Output to this command will show all the four containers coming up

Creating orchestratingdocker_data_1...
Creating orchestratingdocker_postgres_1...
Creating orchestratingdocker_web_1...
Creating orchestratingdocker_nginx_1...
Warning Everytime you run this command a new set of containers will get launched
Connect to PostgreSQL

You can also enter the Postgres Shell – since we forward the port to the host environment in the docker-compose.yml file – to add users/roles as well as databases via:

$ psql -h 127.0.0.1 -p 5432 -U postgres --password
Default password is postgres

Once you are connected, you will notice there are no tables in the database

postgres=# \dt
No relations found.
Create Database Table

We also need to create the database table:

$ docker-compose run web /usr/local/bin/python create_db.py
Once connected to the DB you can run the following command to see the table created

postgres=# \dt
         List of relations
 Schema | Name  | Type  |  Owner
--------+-------+-------+----------
 public | posts | table | postgres
(1 row)
Open your browser and navigate to the IP address associated with Localhost (127.0.0.1):

../_images/screen_shot_1.png
When the posts are made, data gets persisted as shown below

postgres=# select * from posts;
 id |   text   |        date_posted
----+----------+---------------------------
  1 | Hi There | 2015-07-07 07:12:23.39434
Environment Variables

To see which environment variables are available to the web service, run:

$ docker-compose run web env
Logs

To view the logs:

$ docker-compose logs
logs from all the containers are aggregated and shown.

Stopping All Services

To stop the processes using following command

$ docker-compose stop.
Reference

dockerizing-flask-with-compose-and-machine-from-localhost-to-the-cloud



Build a simple Spring Boot app with Docker

In this tutorial we will building a simple Spring Boot application which will run inside a docker container.

Required Software

docker (1.6.0 or above)
jdk 1.8
Gradle 2.3+ or Maven 3.0+
Install the required software

$ sudo add-apt-repository ppa:webupd8team/java
$ sudo apt-get update
$ sudo apt-get install oracle-java8-installer
$ java -version
java version "1.8.0_45"
Java(TM) SE Runtime Environment (build 1.8.0_45-b14)
Java HotSpot(TM) 64-Bit Server VM (build 25.45-b02, mixed mode)
$ sudo apt-get install gradle
$ sudo apt-get install maven
Setup a Spring Boot App

The following project can be cloned from official git repository in order to run the basic example of spring boot application inside a container.

$git clone https://github.com/spring-guides/gs-spring-boot-docker.git
Spring Boot application

The java file can be found at following location;

src/main/java/hello/Application.java

package hello;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.bind.RelaxedPropertyResolver;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@SpringBootApplication
@RestController
public class Application {

        @RequestMapping("/")
        public String home() {
                return "Hello Docker World";
        }


        public static void main(String[] args) {
                SpringApplication.run(Application.class, args);
        }

}
The class is flagged as a @SpringBootApplication and as a @RestController, meaning it’s ready for use by Spring MVC to handle web requests. @RequestMapping maps / to the home() method which just sends a response back. The main() method uses Spring Boot’s SpringApplication.run() method to launch an application.

Containerize the Spring Boot application

We will containerize the above application using the DockerFile. The project JAR file is added to the container as “app.jar” and then executed in the ENTRYPOINT.We have added a VOLUME pointing to /tmp because it is where a Spring Boot application creates working directories for Tomcat by default.

Dockerfile

This file is needed to create a docker image;

FROM java:8
VOLUME /tmp
ADD gs-spring-boot-docker-0.1.0.jar app.jar
RUN bash -c 'touch /app.jar'
ENTRYPOINT ["java","-Djava.security.egd=file:/dev/./urandom","-jar","/app.jar"]
Build a Docker Image with Maven

The maven supports the docker plugin in order to build the docker image. The following three configurations are required in building the docker image either with maven or gradle.

The image name (or tag)
The directory in which to find the Dockerfile
The resources (files) to copy from the target directory to the docker build (alongside the Dockerfile) - we only need the jar file in this example
The maven pom.xml should contain the following configuration;

pom.xml

<properties>
        <docker.image.prefix>springio</docker.image.prefix>
</properties>
<build>
    <plugins>
        <plugin>
            <groupId>com.spotify</groupId>
            <artifactId>docker-maven-plugin</artifactId>
            <version>0.2.3</version>
            <configuration>
                <imageName>${docker.image.prefix}/${project.artifactId}</imageName>
                <dockerDirectory>src/main/docker</dockerDirectory>
                <resources>
                    <resource>
                        <targetPath>/</targetPath>
                        <directory>${project.build.directory}</directory>
                        <include>${project.build.finalName}.jar</include>
                    </resource>
                </resources>
            </configuration>
        </plugin>
    </plugins>
</build>
Using the maven build the docker image

$ mvn package docker:build
Build a Dokcer image with Gradle

Even the gradle provides the plugin to build the docker image. The above mentioned 3 configurations are required to be provided in the build.gradle file

build.gradle

buildscript {
    ...
    dependencies {
        ...
        classpath('se.transmode.gradle:gradle-docker:1.2')
    }
}

group = 'springio'

...
apply plugin: 'docker'

task buildDocker(type: Docker, dependsOn: build) {
  push = true
  applicationName = jar.baseName
  dockerfile = file('src/main/docker/Dockerfile')
  doFirst {
    copy {
      from jar
      into stageDir
    }
  }
}
Using the gradle build the docker image

$ ./gradlew build buildDocker
Run the Spring Boot App container

Now just execute the following command in order to run the containerized application;

$ docker images
REPOSITORY                        TAG                 IMAGE ID            CREATED             VIRTUAL SIZE
gregturn/gs-spring-boot-docker    latest              3e70f57df702        21 hours ago        841.4 MB
$ docker run -p 8080:8080 -t gregturn/gs-spring-boot-docker
The application is now available and can be accessed at the address http://localhost:8080.

Reference

https://spring.io/guides/gs/spring-boot-docker/#initial

