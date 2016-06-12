title: Introduction to Terraform
date: 2016-05-02
description: An introduction to Terraform
tags: terraform, vagrant, packer, kubernets, spark, programming, hadoop, bigdata, yarn


#### What is Terraform?
Terraform by HashiCorp, an APN Technology Partner and AWS DevOps Competency Partner, is an “infrastructure as code” tool similar to AWS CloudFormation that allows you to create, update, and version your AWS infrastructure. Terraform has a great set of features that make it worth adding to your toolbelt, including:

* Friendly custom syntax, but also has support for JSON.
* Visibility into changes before they actually happen.
* Built-in graphing feature to visualize the infrastructure.
* Understands resource relationships. One example is failures are isolated to dependent resources while non-dependent resources still get created, updated, or destroyed.
* Open source project with a community of hundreds of contributors who add features and updates.
* The ability to break down the configuration into smaller chunks for better organization, re-use, and maintainability. The last part of this article goes into this feature in detail.

#### Building Blocks
An advantage of using an infrastructure of code tool is that your configurations also become your documentation.  Breaking down your infrastructure into components makes it easier to read and update your infrastructure as you grow. This, in turn, helps makes knowledge sharing and bringing new team members up to speed easier.

Because Terraform allows you to segment chunks of infrastructure code into multiple files (more on this below), it’s up to you to decide on a logical structure for your plans.  With this in mind, one best practice could be to break up Terraform files by microservice, application, security boundary, or AWS service component. For example, you might have one group of Terraform files that build out an ECS cluster for your inventory API and another group that builds out the Elastic Beanstalk environment for your production front-end web application.

Additionally, Terraform supports powerful constructs called modules that allow you to re-use infrastructure code.  This enables you to provide infrastructure as building blocks that other teams can leverage.  For example, you might create a module for creating EC2 instances that uses only the instance types your company has standardized on.  A service team can then include your module and automatically be in compliance.  This approach creates enablement and promotes self-service.


#### Organizing Complex Services with Modules
Modules are logical groupings of Terraform configuration files.  Modules are intended to be shared and re-used across projects, but can also be used within a project to help better structure a complex service that includes many infrastructure components.  Unfortunately, Terraform does not recursively load files in subdirectories, so you have to use modules to add structure to your project instead of using one large file or multiple smaller files in the same directory.  You can then execute these modules from a single configuration file (we’ll use main.tf for this example) in the parent directory where your sub-directories (modules) are located.  Let’s examine this concept a bit closer.

Modules run sequentially, so you must understand your order of dependencies.  For example, a module to create a launch configuration must run before a module that creates an Auto Scaling group, if the Auto Scaling group depends on the newly created launch configuration.  Each module should be ordered top (first to run) to bottom (last to run) in your main.tf file (more on this later) appropriately.

Terraform allows you to reference output variables from one module for use in different modules. The benefit is that you can create multiple, smaller Terraform files grouped by function or service as opposed to one large file with potentially hundreds or thousands of lines of code.  To use Terraform modules effectively, it is important to understand the interrelationship between output variables and input variables.   At a high level, these are the steps you would take to make an object in one module available to another module:

1. Define an output variable inside a resource configuration (module_A).  The scope of resource configuration details are local to a module until declared as an output.
2. Declare the use of module_A’s output variable in the configuration of another module, module_B. Create a new key name in module_B and set the value equal to the output variable from module_A.
Finally, create a variables.tf file for module_B. In this file, create an input variable with the same name as the key you defined in module_B in step 
3. This variable is what allows dynamic configuration of resource(s) in a module. Because this variable is limited to module_B in scope, you need to repeat this process for any other module that needs to reference module_A’s output.


