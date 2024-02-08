# PiXelTubes

CREATE DATABASE IF NOT EXISTS pixeltube_db;

USE pixeltube_db;

CREATE TABLE IF NOT EXISTS tubes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    mac_address VARCHAR(17) NOT NULL UNIQUE,
    universe INT NOT NULL,
    dmx_address INT NOT NULL,
    CONSTRAINT mac_address_format CHECK (LENGTH(mac_address) = 17 AND mac_address REGEXP '([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})')
);

create user 'pxm'@'localhost' IDENTIFIED by 'pixel';

grant all privileges on pixeltube_db . * to 'pxm'@'localhost';

flush privileges;