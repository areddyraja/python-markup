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

	::text
	terraform show
	aws_instance.example:
	  id = i-00732cee8133775f4
	  ami = ami-a89c4acb
	  availability_zone = ap-southeast-1b
	  disable_api_termination = false
	  ebs_block_device.# = 0
	  ebs_optimized = false
	  ephemeral_block_device.# = 0
	  iam_instance_profile = 
	  instance_state = running
	  instance_type = t2.micro
	  key_name = 
	  monitoring = false
	  private_dns = ip-172-31-26-166.ap-southeast-1.compute.internal
	  private_ip = 172.31.26.166
	  public_dns = ec2-54-169-65-84.ap-southeast-1.compute.amazonaws.com
	  public_ip = 54.169.65.84
	  root_block_device.# = 1
	  root_block_device.0.delete_on_termination = true
	  root_block_device.0.iops = 100
	  root_block_device.0.volume_size = 8
	  root_block_device.0.volume_type = gp2
	  security_groups.# = 0
	  source_dest_check = true
	  subnet_id = subnet-da332ead
	  tags.# = 0
	  tenancy = default
	  vpc_security_group_ids.# = 1
	  vpc_security_group_ids.2305927841 = sg-64a31e00
		
 
#### Show the details

	:::text
	terraform show 
	Refreshing Terraform state prior to plan...

	The Terraform execution plan has been generated and is shown below.
	Resources are shown in alphabetical order for quick scanning. Green resources
	will be created (or destroyed and then created if an existing resource
	exists), yellow resources are being changed in-place, and red resources
	will be destroyed.

	Note: You didn't specify an "-out" parameter to save this plan, so when
	"apply" is called, Terraform can't guarantee this is what will execute.

	+ aws_instance.example
	    ami:                      "" => "ami-a89c4acb"
	    availability_zone:        "" => "<computed>"
	    ebs_block_device.#:       "" => "<computed>"
	    ephemeral_block_device.#: "" => "<computed>"
	    instance_state:           "" => "<computed>"
	    instance_type:            "" => "t2.micro"
	    key_name:                 "" => "<computed>"
	    placement_group:          "" => "<computed>"
	    private_dns:              "" => "<computed>"
	    private_ip:               "" => "<computed>"
	    public_dns:               "" => "<computed>"
	    public_ip:                "" => "<computed>"
	    root_block_device.#:      "" => "<computed>"
	    security_groups.#:        "" => "<computed>"
	    source_dest_check:        "" => "true"
	    subnet_id:                "" => "<computed>"
	    tenancy:                  "" => "<computed>"
	    vpc_security_group_ids.#: "" => "<computed>"


	Plan: 1 to add, 0 to change, 0 to destroy.

#### Make it so.. 
	
	:::text
	terraform apply 

will execute the file and create instance 

	::text
	aws_instance.example: Creating...
	  ami:                      "" => "ami-a89c4acb"
	  availability_zone:        "" => "<computed>"
	  ebs_block_device.#:       "" => "<computed>"
	  ephemeral_block_device.#: "" => "<computed>"
	  instance_state:           "" => "<computed>"
	  instance_type:            "" => "t2.micro"
	  key_name:                 "" => "<computed>"
	  placement_group:          "" => "<computed>"
	  private_dns:              "" => "<computed>"
	  private_ip:               "" => "<computed>"
	  public_dns:               "" => "<computed>"
	  public_ip:                "" => "<computed>"
	  root_block_device.#:      "" => "<computed>"
	  security_groups.#:        "" => "<computed>"
	  source_dest_check:        "" => "true"
	  subnet_id:                "" => "<computed>"
	  tenancy:                  "" => "<computed>"
	  vpc_security_group_ids.#: "" => "<computed>"
	aws_instance.example: Still creating... (10s elapsed)
	aws_instance.example: Still creating... (20s elapsed)
	aws_instance.example: Creation complete

	Apply complete! Resources: 1 added, 0 changed, 0 destroyed.

	The state of your infrastructure has been saved to the path
	below. This state is required to modify and destroy your
	infrastructure, so keep it safe. To inspect the complete state
	use the `terraform show` command.

	State path: terraform.tfstate

#### Show the details

	:::text
	terraform show 

to get the details of newly created instance 

	::text
	aws_instance.example:
	  id = i-0378bfe455ce45520
	  ami = ami-a89c4acb
	  availability_zone = ap-southeast-1b
	  disable_api_termination = false
	  ebs_block_device.# = 0
	  ebs_optimized = false
	  ephemeral_block_device.# = 0
	  iam_instance_profile = 
	  instance_state = running
	  instance_type = t2.micro
	  key_name = 
	  monitoring = false
	  private_dns = ip-172-31-24-114.ap-southeast-1.compute.internal
	  private_ip = 172.31.24.114
	  public_dns = ec2-54-179-165-32.ap-southeast-1.compute.amazonaws.com
	  public_ip = 54.179.165.32
	  root_block_device.# = 1
	  root_block_device.0.delete_on_termination = true
	  root_block_device.0.iops = 100
	  root_block_device.0.volume_size = 8
	  root_block_device.0.volume_type = gp2
	  security_groups.# = 0
	  source_dest_check = true
	  subnet_id = subnet-da332ead
	  tags.# = 0
	  tenancy = default
	  vpc_security_group_ids.# = 1
	  vpc_security_group_ids.2305927841 = sg-64a31e00
	
 
#### Terraform state file
Terraform saves the state of the infrastrcuture in the file.

	:::text
	# vi terraform.tfstate 
	 
You can also check the default file for instance details 

#### Destroy the instance
	:::text
	 terraform destroy
	Do you really want to destroy?
	  Terraform will delete all your managed infrastructure.
	  There is no undo. Only 'yes' will be accepted to confirm.

	  Enter a value: yes


	Apply complete! Resources: 0 added, 0 changed, 0 destroyed.

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



