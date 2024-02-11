# PiXelTubes

### A little introduction :)

PiXelTubes is a little fun project for me. **(CURRENTLY WORK IN PROGRESS)**

It is inspired by the Astera Helios/Titan tubes. The most classic, state of the art LED tubes for event lighting.

So maybe the question comes up, why I don't just buy some of them and use them. For me a big problem is the price and also I wanted a little project for my holiday week. So I thought why not build a cheap alternative with some led strips and some Raspberry Pi's.

BTW excuse the very "creative" name, but every Raspberry Pi project has to have a "Pi" in it's name.

For this project you will need a soldering iron and atleast a bit of knowledge on how to solder because you will have to solder the strip to the Raspberry Pi Zero.









### Before we start with what you need to build your own PiXelTube system here are some ideas on how to integrate those PiXelTubes.

For the beginners or "newbies" to lighting you can use free solutions like QLC+ for a small setup. Only problem with QLC+ is that pixel control is a bit complex.

If you want to be a bit more professional but don't want to pay any money you can use MA Lighting dot2. Still pixel control is a bit of a hassle but if you get it running it is awsome. There are some good online courses out there for the software. It is kind of semi-professional, so you have to get a bit more into the rabbit hole.

For the professionals out there, most of you will already know how to pixel control/map such fixtures but here is a list of the software I would recommend:

* MADRIX (Made specificly for pixel mapping/control.)
* Resolume Arena (Originally made for visual playback but you can output DMX to such pixel fixtures and map you visuals to them.)
* grandMA3 (If you already spend all your money on that sweet little onPC node it is still a good solution. I mean the selection grid is a good way to map the pixels as subfixtures)
* grandMA2 (I personally havn't used grandMA2 because I started with grandMA3 but I think it would also be possible to map the pixels in some do-able way.)
* Software I only heard of but that also should work:
  * ENTTEC LED MAPPER (ELM)
  * PIXXEM
  * MadMapper
  * Touchdesigner


### The fixture profiles for various solutions:

* grandMA3 GDTF: **work in progress**
* grandMA2/dot2: **work in progress**
* Resolume Arena: **work in progrss**


### What you need on the hardware side:

* As a master server I am using a Raspberry Pi 4 B 4GB. You can probably use somthing smaller, but I haven't tested that right now.
* MicroSD card (16gb recommended)
* Raspberry Pi 4 power supply (I have the official one)
* Raspberry Pi 4 case (also here the official one)
* Raspberry Pi 4 fan (optional, but recommended. I have the pimoroni one *not sponsored*)
* For the tubes I am using:
  * WS2812B LED strip (1 meter, 30 LEDs) (I don't put a link here because I bought them off of eBay and maybe the seller doesn't sell them in the future. Just google "WS2812B LED strip 30 leds 1m". On eBay they are most of the time even cheaper then on chinese sites.)
  * Raspberry Pi Zero W
  * Small powerbank (idk just look for something that fits your usage and online time)
  * Raspberry Pi Zero Case (I have the official one)
  * Some wire for soldering the strip
  * And you need a defusor tube for the strip (I am still looking for one so if I find one I am going to also put a link here)


sudo apt install python3 python3-pip git python3-flask python3-flask-mysqldb python3-adafruit-circuitpython-neopixel python3-wifi apache2 php mariadb-server mariadb-client -y

sudo mysql -u root -p
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

sudo systemctl restart apache2
