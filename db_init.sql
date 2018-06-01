-- db initialization 

CREATE DATABASE student; 

-- user init
CREATE ROLE init WITH LOGIN PASSWORD 'qwerty';
GRANT ALL PRIVILEGES ON DATABASE student TO init;


-- user app
CREATE ROLE app WITH LOGIN PASSWORD 'qwerty';
GRANT ALL PRIVILEGES ON DATABASE student TO app;

-- pgcrypto for storing passwords safely 
CREATE EXTENSION pgcrypto;