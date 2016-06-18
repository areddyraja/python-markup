title: Auto Scaling Group with Terraform
date: 2016-05-02
description: An introduction to Terraform
tags: terraform, vagrant, packer, kubernets, spark, programming, hadoop, bigdata, yarn

#### Terraform scripts for Auto Scaling Group
This creates a security group, launch configuration, auto scaling group and an ELB. The user data for launch configuration installs nginx and it listens on port 80.
The example uses latest Ubuntu AMIs.


To run, configure your AWS provider as described in https://www.terraform.io/docs/providers/aws/index.html
#### Define the variables

open file varables.tf and paste the following lines.

	:::text
	variable "aws_region" {
	  description = "The AWS region to create things in."
	  default = "us-east-1"
	}

	# ubuntu-trusty-14.04 (x64)
	variable "aws_amis" {
	  default = {
	    "us-east-1" = "ami-5f709f34"
	    "us-west-2" = "ami-7f675e4f"
	  }
	}

	variable "availability_zones" {
	  default = "us-east-1b,us-east-1c,us-east-1d,us-east-1e"
	  description = "List of availability zones, use AWS CLI to find your "
	}

	variable "key_name" {
	  description = "Name of AWS key pair"
	}

	variable "instance_type" {
	  default = "t2.micro"
	  description = "AWS instance type"
	}

	variable "asg_min" {
	  description = "Min numbers of servers in ASG"
	  default = "1"
	}

	variable "asg_max" {
	  description = "Max numbers of servers in ASG"
	  default = "2"
	}

	variable "asg_desired" {
	  description = "Desired numbers of servers in ASG"
	  default = "1"
	}

Make sure you change the list of availability zones that is applicable to your account and region.

#### Create Auto Scalaing Group

open main.tf and copy the following contents

	:::text
	# Specify the provider and access details
	provider "aws" {
	  region = "${var.aws_region}"
	}

	resource "aws_elb" "web-elb" {
	  name = "terraform-example-elb"

	  # The same availability zone as our instances
	  availability_zones = ["${split(",", var.availability_zones)}"]
	  listener {
	    instance_port = 80
	    instance_protocol = "http"
	    lb_port = 80
	    lb_protocol = "http"
	  }

	  health_check {
	    healthy_threshold = 2
	    unhealthy_threshold = 2
	    timeout = 3
	    target = "HTTP:80/"
	    interval = 30
	  }

	}

	resource "aws_autoscaling_group" "web-asg" {
	  availability_zones = ["${split(",", var.availability_zones)}"]
	  name = "terraform-example-asg"
	  max_size = "${var.asg_max}"
	  min_size = "${var.asg_min}"
	  desired_capacity = "${var.asg_desired}"
	  force_delete = true
	  launch_configuration = "${aws_launch_configuration.web-lc.name}"
	  load_balancers = ["${aws_elb.web-elb.name}"]
	  #vpc_zone_identifier = ["${split(",", var.availability_zones)}"]
	  tag {
	    key = "Name"
	    value = "web-asg"
	    propagate_at_launch = "true"
	  }
	}

	resource "aws_launch_configuration" "web-lc" {
	  name = "terraform-example-lc"
	  image_id = "${lookup(var.aws_amis, var.aws_region)}"
	  instance_type = "${var.instance_type}"
	  # Security group
	  security_groups = ["${aws_security_group.default.id}"]
	  user_data = "${file("userdata.sh")}"
	  key_name = "${var.key_name}"
	}

	# Our default security group to access
	# the instances over SSH and HTTP
	resource "aws_security_group" "default" {
	  name = "terraform_example_sg"
	  description = "Used in the terraform"

	  # SSH access from anywhere
	  ingress {
	    from_port = 22
	    to_port = 22
	    protocol = "tcp"
	    cidr_blocks = ["0.0.0.0/0"]
	  }

	  # HTTP access from anywhere
	  ingress {
	    from_port = 80
	    to_port = 80
	    protocol = "tcp"
	    cidr_blocks = ["0.0.0.0/0"]
	  }

	  # outbound internet access
	  egress {
	    from_port = 0
	    to_port = 0
	    protocol = "-1"
	    cidr_blocks = ["0.0.0.0/0"]
	  }
	}

#### Create output variable file
open output.tf and copy the following code

	:::text
	output "security_group" {
	  value = "${aws_security_group.default.id}"
	}
	output "launch_configuration" {
	  value = "${aws_launch_configuration.web-lc.id}"
	}
	output "asg_name" {
	  value = "${aws_autoscaling_group.web-asg.id}"
	}
	output "elb_name" {
	  value = "${aws_elb.web-elb.dns_name}"
	}

#### Create user data script
Open file userdata.sh and copy the following contents

	:::text
	#!/bin/bash -v
	apt-get update -y
	apt-get install -y nginx > /tmp/nginx.log



### Running the example

#### For planning phase

	:::text
	terraform plan -var 'key_name={your_key_name}}'

#### For apply phase

	:::text
	terraform apply -var 'key_name={your_key_name}}'

Once the stack is created, wait for few minutes and test the stack by launching a browser with ELB url.

#### To remove the stack

	:::text
	terraform destroy -var 'key_name={your_key_name}}'


