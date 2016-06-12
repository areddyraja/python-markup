title: Installing MySQL
date: 2016-05-02
description: Installing MySQL in Ubuntu
tags: All you want about MySQL is here


### Install mysql on ubuntu 14.04 -----

##### Before going to install mysql check your hostname. 

    $ hostname 

##### Then update your system by using the below commands: 

    $ sudo apt-get update 

    $ sudo apt-get upgrade 

##### Next install mysql as 

    $ sudo apt-get install mysql-server  

    During the installation process, you will be prompted to set a     password for the MySQL root user. Choose a strong password and keep it in a safe place for future reference. 

##### Run the mysql_secure_installation script to address several security concerns in a default MySQL installation: 

    $ sudo mysql_secure_installation 

   You will be given the choice to change the MySQL root password, remove anonymous user accounts, disable root logins outside of localhost, and remove test databases. It is recommended that you answer yes to these options. 

  Now mysql is ready, you can use it by following the below steps. 

##### Use MySQL: 

  The standard tool for interacting with MySQL is the mysql client, which installs with the mysql-server package. The MySQL client is accessed through a terminal. 

##### To log in to MySQL as the root user:
    $ mysql -u root -p 

     When prompted, enter the root password you assigned when the mysql_secure_installation script was run. 

     You’ll then be presented with the MySQL monitor prompt: 

##### To generate a list of commands for the MySQL prompt, enter \h.
     
     mysql> \h 

##### To check all databases run: 

     mysql> show databases; 

      It will list the default databases that are present with the installation. 

##### Create a new database and create a table within it with some data: 

  mysql> create database testdb; -----> to create new db with the name testdb

       > use testdb;  -----> to enter into the db 

       > show tables; -----> to check the tables

       > create table sales(id int,name char(64), sal int); -----> create table sales with the column name id, name and sal 

       > desc sales; -----> to describe the schema of sales table 

       > select * from sales; -----> to read the details in sales table. But as I created this table now, so no data is present. Let us insert the details into the table. 

       > insert into sales values(100,'dax',10000); 

    It will add the details of dax into the table. 

       > select * from sales; 
    
    Now we can able to see one record under sales table. 

       > insert into sales(id,name) values (102, 'tom');
    
    To insert the value to the specific field. 

       > update sales set sal=5000 where id=102; 

    It will add 5000 as sal for tom user. You can update the existing fields also by using the same format. 

       > delete from sales where name='dax'; 

    To delete the record from table. You can use any field to delete the record using where clause but make sure you are deleting the correct one. 
 
       > drop table sales; -----> to delete the whole table

#### Create a New MySQL User: 

##### Login to mysql with root credentials and execute the below command 

   mysql> create user testuser@localhost identified by "test123"; 

  It will create testuser with password test123. The user's detail information will be stored under user table within default mysql database. 

        > use mysql;
        > select * from user where user='testuser'; 

##### By default the users will not have any privileges. so we need to grant the permission. 

        > grant all on *.* to testuser@localhost; 

   It will give all permission to all db and tables. You can grant a specific permission as your requirement. 

#####    > flush privileges; -----> to update the new privileges 

##### Now login to that user and check the permissions. 
      
       $ mysql -u testuser -p  (give testuser password to login) 
       
     You can run mysql queries to check whether you have privileges over all db or not. 

##### To check the grants for a user run
   
      > show grants for testuser@localhost; ----> you can able to see the permissions 

##### To remove the privileges execute
  
      > revoke all on *.* from testuser@localhost;
      > flush privileges; -----> to update the privileges 

##### To delete a user run 

      > drop user testuser@localhost; 

      You can confirm that the user doesn't exist, by checking the user table under mysql db. 

      > exit -----> to quit mysql prompt 

#### Reset the MySQL Root Password: 

  If you forget your MySQL root password, it can be reset.

##### Stop the current MySQL server instance: 
   
      $ sudo service mysql stop 

##### Use dpkg to re-run the configuration process that MySQL goes through on first installation. You will again be asked to set a root password. 

      $ sudo dpkg-reconfigure mysql-server-5.5 

##### Then start MySQL: 

      $ sudo service mysql start 

   You’ll now be able to log in again using "mysql -u root -p" with the new password.


