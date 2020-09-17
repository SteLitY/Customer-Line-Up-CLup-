use dc2633; #temporarily using IBM from Hunter. You can use your own db to test for now

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

#line for the customers... needs some looking over
CREATE TABLE IF NOT EXISTS queue(
groupID INT AUTO_INCREMENT,
numOfCustomers INT NOT NULL,
dt date,
companyID INT UNIQUE NOT NULL,
userID INT UNIQUE NOT NULL, #remove not null if you allow same client to go on the same line twice in a day. Maybe they have a lot to buy and need to make 2 trips or maybe we don't want the person to reserve too many spots (ex: idiot pressing the "enter queue" button too many times thinking it's not working)
placeInLine INT
);


