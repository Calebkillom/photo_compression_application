-- create database if it does not exist
CREATE DATABASE IF NOT EXISTS webapp_dev_db;

-- create user if it does not exist
CREATE USER IF NOT EXISTS webapp_dev@localhost IDENTIFIED BY 'webapp_dev_pwd';

-- create user if it does not exist
GRANT ALL PRIVILEGES ON webapp_dev_db.* TO webapp_dev@localhost;

-- grant SELECT privilege to the user for performance_schema database
GRANT SELECT ON performance_schema.* TO webapp_dev@localhost;
