-- MariaDB script

-- Drop the database if it exists
DROP DATABASE IF EXISTS social_media;

-- Create the database
CREATE DATABASE social_media;

-- Use the database
USE social_media;

-- Table 'UserData'
DROP TABLE IF EXISTS UserData;

CREATE TABLE UserData (
    id CHAR(36) NOT NULL PRIMARY KEY,
    data VARCHAR(160) NOT NULL
);