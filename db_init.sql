-- db initialization 

CREATE DATABASE student; 

-- user init
CREATE ROLE init WITH CREATEROLE LOGIN PASSWORD 'qwerty';
GRANT ALL PRIVILEGES ON DATABASE student TO init;

-- pgcrypto for storing passwords safely 
-- must be superuser to execute this command
CREATE EXTENSION pgcrypto;