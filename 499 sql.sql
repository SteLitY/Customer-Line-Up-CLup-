#This is currently using Azure  -David 9/22/2020
#This code to checks if data was inputted into the MySQL tables properly

CREATE DATABASE IF NOT EXISTS lineup;
show databases;

select * from COLLATIONS;
use information_schema;
show tables;
use mysql;
show tables;
use clup;
show tables;

select * from clup.auth_user;
select * from auth_group;
desc auth_user;

truncate posts_customer_queue;

UPDATE auth_user
SET is_staff=1
WHERE username = "David2";

desc clup.posts_customer_queue;

select * from clup.posts_customer_queue;
select * from clup.posts_customer;
select * from clup.auth_user;
select * from clup.posts_profile;
select * from clup.posts_business;
desc clup.posts_business;
select * from posts_post;

show tables;
drop table posts_all_customers;

select store_name, sum(select group_size from posts_customer_queue where store_name=store_name)  from posts_customer_queue;

SET SQL_SAFE_UPDATES = 0;
select * from django_session;
select * from django_admin_log;

select * from django_content_type;
delete from django_content_type where app_label = 'posts';

select * from django_migrations;
delete from django_migrations where app = 'sessions';


select * from posts_post;
select * from posts_test;
select * from django_session;
select * from django_migrations;
select * from django_content_type;
select * from django_admin_log;
select * from auth_user_user_permissions;
select * from auth_permission;
select * from posts_post;
select * from posts_post;
select * from auth_group_permissions;
select * from auth_user;
use sys;
desc auth_group;
select * from auth_group;
drop database clup;
drop database lineup;

CREATE DATABASE clup CHARACTER SET UTF8;
CREATE USER David@lineup499.mysql.database.azure.com IDENTIFIED BY 'username';
GRANT ALL PRIVILEGES ON clup.* TO David@lineup499.mysql.database.azure.com;

#Register a client
CREATE TABLE IF NOT EXISTS customers(
customerID INT AUTO_INCREMENT PRIMARY KEY,
password varchar(32) NOT NULL,
firstName varchar(64) NOT NULL,
middleName varchar(64),
lastName varchar(64) NOT NULL,
email varchar(32) UNIQUE NOT NULL,
cellnumber varchar(12) NOT NULL 
);
#Testing the customers table
#duplicate email and making sure null works for some.
-- insert into customers (password, firstName, lastName, email, cellnumber) VALUES ("password1234", "David", "Chen", "myemail@dns.com" ,"911");
-- insert into customers (password, firstName, lastName, email, cellnumber) VALUES ("password1234", "Tom", "Audo", "myemail@dns.com" ,"311"); 
-- select * from customers;
-- truncate table customers;
-- drop table customers;

#Register a company
CREATE TABLE IF NOT EXISTS company(
companyID INT AUTO_INCREMENT UNIQUE,
companyName varchar(32) NOT NULL,
companyAddress varchar(128) NOT NULL,
companyZipcode varchar(5) NOT NULL,
storeCapacity int NOT NULL,
companyPhone varchar(12) NOT NULL,
companyEmail varchar(32) NOT NULL
); #owner contact info can be found in table "companyContactInfo"

#prevents repeating data
CREATE TABLE IF NOT EXISTS zipcode(
zipCode varchar(5),
city varchar(32),
state varchar(32),
);

#Table to store the contact info of managers/owners. It's for the develoeprs to call the manager/company. Remember that one person can own multiple stores
CREATE TABLE IF NOT EXISTS companyContactInfo(
ownerID INT NOT NULL AUTO_INCREMENT,
ownerLastName varchar(128) NOT NULL,
ownerMiddleName varchar(128),
ownerFirstName varchar(128) NOT NULL,
ownerEmail varchar(32) NOT NULL,
ownerCell varchar(12) NOT NULL
);


#This table links the company to the company contact info. Prevents repeating data. One company can have multiple contact people (ex: day+evening manager) or one person can own multiple stores
CREATE TABLE IF NOT EXISTS companyContactDetails
(
ownerID INT,
companyID INT
);

#New table to handle different hours for different days (ex: 9-5 M-F, but 10-4 on weekends)
CREATE TABLE IF NOT EXISTS companyHours(
companyID INT,
dayOfWeek INT(1), #Note: 1=Sunday, 2=Monday, 3=Tuesday, 4=Wednesday, 5=Thursday, 6=Friday, 7=Saturday using DAYOFWEEK(DayOfWeek) Documentation: https://www.w3schools.com/sql/func_mysql_dayofweek.asp
startTime TIME, #format is 'hh:mm:ss'. Not unique because you can have multiple hours for the same day. ex: a restaurant that opens 4 AM to 11 AM, then reopen at 5 PM up until 12 PM.
endTime TIME
);
#Testing companyHours table
-- INSERT INTO companyHours (companyID, dayOfWeek, startTime,endTime) VALUES (123, 1, '9:11', '5:12'); #This company is opened from 9:11 to 5:!2 on Sundays
-- INSERT INTO companyHours (companyID, dayOfWeek, startTime,endTime) VALUES (123, 2, '3:11', '8:12'); #The same company is opened from 3:11 to 8:12 on Mondays
-- select * from companyHours;

#line for the customers... needs some looking over. use SELECT MIN to find the person next on line. 
CREATE TABLE IF NOT EXISTS queue(
groupID INT AUTO_INCREMENT,
numInGroup INT NOT NULL,
dt date,
companyID INT UNIQUE NOT NULL,
userID INT UNIQUE NOT NULL, #remove not null if you allow same client to go on the same line twice in a day. Maybe they have a lot to buy and need to make 2 trips or maybe we don't want the person to reserve too many spots (ex: idiot pressing the "enter queue" button too many times thinking it's not working)
placeInLine INT
);

