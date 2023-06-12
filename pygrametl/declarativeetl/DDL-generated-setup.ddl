-- This file was generated by PygramETL-DeclarativeETL (https://github.com/smath17/declarative-etl)

CREATE DATABASE test;
\connect test

CREATE TABLE Customer_Dimension
(
CustomerKEY SERIAL PRIMARY KEY,
name VARCHAR(30),
address VARCHAR(30)
);

CREATE TABLE Part_Dimension
(
PartKEY SERIAL PRIMARY KEY,
name VARCHAR(30),
manufacturer VARCHAR(30)
);

CREATE TABLE Date_Dimension
(
DateKEY SERIAL PRIMARY KEY,
day INT,
month INT,
year INT
);

CREATE TABLE Lineorder_Fact_Table
(
CustomerKEY SERIAL REFERENCES Customer_Dimension,
PartKEY SERIAL REFERENCES Part_Dimension,
CommitDate SERIAL REFERENCES Date_Dimension,
ShippingDate SERIAL REFERENCES Date_Dimension,
PRIMARY KEY (CustomerKEY, PartKEY, CommitDate, ShippingDate),
quantity INT,
price DECIMAL(10, 4)
);
