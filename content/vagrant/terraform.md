title: Terraform Tutorial
date: 2016-05-02
description: A tutorial on Terraform
tags: terraform, aws, provisioningo

The tutorial gives a detail steps of using Terraform to create AWS intances.

#### Download Terraform

Download Terraform from the below link
https://www.terraform.io/downloads.html 
  
#### Install Terraform
Install it by following the link
https://www.terraform.io/intro/getting-started/install.html 
 
#### Set the Path
Set the path as 
PATH=/usr/local/terraform:/root/terraform:$PATH 
  
where /usr/local/terraform will contain all the terraform script files that are unziped from the downloaded zipped file.
  
	:::text
	#terraform (It should not give any error like command not found) 
	
#### Set the provider
  
Get the below keys from your AWS account

	:::text
     Access Key ID: your_key
     Secret Access Key: secret_key
	 
	 
Create a file named like main.tf and add the text 
 
	:::test
	provider "aws" {
	    access_key = "ACCESS_KEY_HERE"
	    secret_key = "SECRET_KEY_HERE"
	    region = "ap-southeast-1"
	}

#### Adding a Resource 

Add the following lines to main.tf 

	:::test
	resource "aws_instance" "example" {
	    ami = "ami-a89c4acb"
	    instance_type = "t2.micro"
	}


#### Make a Plan 

	:::text
	terraform plan 

check the syntax error of .tf file
 
#### Make it so.. 
	
	:::text
	terraform apply 

will execute the file and create instance 
 
#### Show the details

	:::text
	terraform show 

to get the details of newly created instance 
 
#### Terraform state file
Terraform saves the state of the infrastrcuture in the file.

	:::text
	# vi terraform.tfstate 
	 
You can also check the default file for instance details 

#### Change the infrastrcuture

To change the infrastructure go to the .tf file and modify it with a new ami id.
     
#### Make the plan and apply

	:::text
 	#terraform plan //+ means it will recreate the resource)
	#terraform apply //It will terminate the old instance and create the new instance from new ami) 
 	#terraform show  //check new instance properties ) 
 
#### Destroy the infrastructure
To destroy the infrastructure 
 
	:::text
	#terraform plan // -destroy ( to check what resource will destroy)
	#terraform destroy // --> to destroy 



