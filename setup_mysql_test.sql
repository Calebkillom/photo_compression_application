-- Create the database if it doesn't exist
CREATE DATABASE IF NOT EXISTS webapp_test_db;

-- Create the user if it doesn't exist
CREATE USER IF NOT EXISTS webapp_test@localhost IDENTIFIED BY 'webapp_test_pwd';

-- Grant all privileges on the database to the user
GRANT ALL PRIVILEGES ON webapp_test_db.* TO webapp_test@localhost;

-- Grant SELECT privilege on performance_schema to the user
GRANT SELECT ON performance_schema.* TO webapp_test@localhost;
