use dc2633;

CREATE TABLE IF NOT EXISTS customers(
userID INT AUTO_INCREMENT UNIQUE,
password varchar(32),
firstName varchar(64),
middleName varchar(64),
lastName varchar(64),
address varchar,
zipCode varchar(5)
);

CREATE TABLE IF NOT EXISTS zipcode(
zipCode varchar(5),
city varchar(32),
state varchar(32),
);