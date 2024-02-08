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

# Install Flask for the web server
sudo apt-get install python3-flask

# Install Flask-MySQLdb for MySQL integration with Flask
sudo apt-get install python3-flask-mysqldb

# Install python-osc for handling Art-Net messages
sudo apt-get install python3-osc

# Install neopixel library for controlling WS2812B LED strip
sudo apt-get install python3-rpi-ws281x python3-adafruit-circuitpython-neopixel

# Install wifi library for Wi-Fi management
sudo apt-get install python3-wifi
