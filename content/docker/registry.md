Docker Registry

Docker allows to bundle and push the customized images on the docker hub or locally hosted docker registry. Images can be pushed or pull from this registry.

Create official Docker Hub account

$ sudo docker login
Username: username
Password:
Email: email@blank.com
WARNING:login credentials saved in /home/username/.dockercfg.
Account created. Please use the confirmation link we sent to your e-mail to activate it.
Search available images in the Docker hub registry

$ sudo docker search centos
NAME                                DESCRIPTION                                     STARS     OFFICIAL   AUTOMATED
centos                              The official build of CentOS.                   1057      [OK]
ansible/centos7-ansible             Ansible on Centos7                              43                   [OK]
tutum/centos                        Centos image with SSH access. For the root...   13                   [OK]
blalor/centos                       Bare-bones base CentOS 6.5 image                9                    [OK]
jdeathe/centos-ssh-apache-php       CentOS-6 6.6 x86_64 / Apache / PHP / PHP m...   9                    [OK]
torusware/speedus-centos            Always updated official CentOS docker imag...   5                    [OK]
It will list all publically available images having the keyword “centos” in the Docker Hub registry.

Push customized image to Docker repository

$ sudo docker push username/newimage
The push refers to a repository [username/newimage] (len: 1)
d94fdd926b02: Image already exists
accbaf2f09a4: Image successfully pushed
aa354fc0b2b2: Image successfully pushed
3a94f42115fb: Image successfully pushed
7771ee293830: Image successfully pushed
fa81ed084842: Image successfully pushed
e04c66a223c4: Image successfully pushed
7e2c5c55ef2c: Image successfully pushed
.......................................
Please note repository name should meet the username of the docker hub account in order to push the images. Currently docker gives one private repository for free. Otherwise, in general images which are pushed to docker hub account will be made publically available.

Install Private Local Docker Registry

$ docker run -p 5000:5000 registry
Tag the images

Now, we will the tag the same image created in the above tutorial to “localhost:5000/newimage” so that the repository name matches and it can be easily pushed to private docker registry.

$docker tag username/newimage:latest localhost:5000/newimage:latest
Push the image to private docker registry

$ docker push localhost:5000/newimage:latest
The push refers to a repository [localhost:5000/test_nginx_image] (len: 1)
Sending image list
Pushing repository localhost:5000/test_nginx_image (1 tags)
e118faab2e16: Image successfully pushed
7e2c5c55ef2c: Image successfully pushed
e04c66a223c4: Image successfully pushed
fa81ed084842: Image successfully pushed
7771ee293830: Image successfully pushed
3a94f42115fb: Image successfully pushed
aa354fc0b2b2: Image successfully pushed
accbaf2f09a4: Image successfully pushed
d94fdd926b02: Image successfully pushed
Pushing tag for rev [d94fdd926b02] on {http://localhost:5000/v1/repositories/test_nginx_image/tags/latest}
Image ID can be seen by visitng the link in browser or using the curl command which comes up after pushing the image.

