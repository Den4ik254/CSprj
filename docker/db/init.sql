CREATE USER cloudstorage WITH PASSWORD 'eRQWVo93okHPxEaJ';
-- CREATE USER 'cloudstorage'@'localhost' IDENTIFIED BY 'eRQWVo93okHPxEaJ!';


CREATE DATABASE cloudstoragedb;
GRANT ALL PRIVILEGES ON DATABASE cloudstoragedb TO cloudstorage;
-- GRANT ALL PRIVILEGES ON cloudstoragedb . * TO 'cloudstorage'@'localhost';
