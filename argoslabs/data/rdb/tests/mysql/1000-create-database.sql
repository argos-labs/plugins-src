-- create database
CREATE DATABASE mytest;

-- create user
CREATE USER 'myuser'@'%' IDENTIFIED BY 'myuser123!@#';

-- grant user with privileges
GRANT ALL PRIVILEGES ON mytest.* TO 'myuser'@'%' WITH GRANT OPTION;

