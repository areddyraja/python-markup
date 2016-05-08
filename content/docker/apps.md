Static site on Apache server from Docker

In this lab we learn how to host a static site running on Apache server hosted by Docker

Create a Dockerfile

FROM httpd:2.4
COPY ./public-html/ /usr/local/apache2/htdocs/
Create a directory public_html with the following content in index.html

<html>
<body>
Hi There - Static page served by Apache Server
</body>
</html>
Your directory should look like this

$ tree .
.
├── Dockerfile
└── public-html
    └── index.html
Create a Docker image

$ docker build -t my-apache2 .
This will create a my-apache2 image.

Create a Docker Container running this image

docker run  -p 80:80 --name my-apache2-1  my-apache2
Open browser of the host at http://localhost:80, you will see the website up and running

