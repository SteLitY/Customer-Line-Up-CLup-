use dc2633;

CREATE TABLE IF NOT EXISTS customers(
userID INT AUTO_INCREMENT UNIQUE,
password varchar(32),
firstName varchar(64),
middleName varchar(64),
lastName varchar(64),
address varchar(255),
zipCode varchar(5)
);

#Testing table above table
-- insert into customers (password, firstName, middleName, lastName, address, zipCode) VALUES ("1234", "David", "middle", "Chen", "12as" ,"11235");
-- select * from customers;


CREATE TABLE IF NOT EXISTS zipcode(
zipCode varchar(5),
city varchar(32),
state varchar(32),
);

