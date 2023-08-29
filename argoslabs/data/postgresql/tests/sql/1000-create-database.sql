-- https://judo0179.tistory.com/96

-- create database
-- CREATE DATABASE mytest;

-- create user
-- CREATE USER 'myuser'@'%' IDENTIFIED BY 'myuser123!@#';

-- grant user with privileges
-- GRANT ALL PRIVILEGES ON mytest.* TO 'myuser'@'%' WITH GRANT OPTION;

$ docker exec -it postgres /bin/bash

root@ac61c662ee4c:/# psql -U postgres
psql (13.0 (Debian 13.0-1.pgdg100+1))
Type "help" for help.

postgres=# CREATE USER seongwon PASSWORD '1q2w3e4r' SUPERUSER;
CREATE ROLE

postgres=# CREATE DATABASE test OWNER seongwon;
CREATE DATABASE

postgres=# \c test seongwon
You are now connected to database "test" as user "seongwon".
test=# CREATE TABLE star (
id integer NOT NULL,
name character varying(255),
class character varying(32),
age integer,
radius integer,
lum integer,
magnt integer,
CONSTRAINT star_pk PRIMARY KEY (id)
);
CREATE TABLE

test=# \dt
        List of relations
 Schema | Name | Type  |  Owner
--------+------+-------+----------
 public | star | table | seongwon
(1 row)
