-- create table


DROP SEQUENCE IF EXISTS seq_bar_id;
CREATE SEQUENCE seq_bar_id;

DROP TABLE IF EXISTS bar;
CREATE TABLE bar (
  id BIGINT NOT NULL default nextval('seq_foo_id'),
  name VARCHAR(30) NOT NULL,
  age INT NOT NULL,
  PRIMARY KEY (id)
);

