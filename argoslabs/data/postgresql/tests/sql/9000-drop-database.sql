-- grant user with privileges
REVOKE ALL ON mytest.* FROM 'myuser'@'%';

-- drop user
DROP USER 'myuser'@'%';

-- drop database
DROP DATABASE mytest;

