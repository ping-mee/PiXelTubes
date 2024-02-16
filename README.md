# PiXelTubes

### A little introduction :)

PiXelTubes is a little fun project for me. **(CURRENTLY WORK IN PROGRESS)**

It is inspired by the Astera Helios/Titan tubes. The most classic, state of the art LED tubes for event lighting.

So maybe the question comes up, why I don't just buy some of them and use them. For me a big problem is the price and also I wanted a little project for my holiday week. So I thought why not build a cheap alternative with some led strips and some Raspberry Pi's.

BTW excuse the very "creative" name, but every Raspberry Pi project has to have a "Pi" in it's name.

For this project you will need a soldering iron and atleast a bit of knowledge on how to solder because you will have to solder the strip to the Raspberry Pi Zero.

### Before we start with what you need to build your own PiXelTube system here are some ideas on how to integrate those PiXelTubes.

**DISCLAIMER:** I am not sponsored by an company/software I am mentioning. These are just recommendations ;)

For the beginners or "newbies" in the lighting niche you can use free solutions like QLC+ for a small setup. The only problem with QLC+ is that pixel control is a bit complex.

If you want to be a bit more professional but don't want to pay any money you can use MA Lighting dot2. Still pixel control is a bit of a hassle but if you get it running it is awesome. There are some good online courses out there for the software. It is kind of semi-professional, so you have to get a bit more into the rabbit hole.

For the professionals out there, most of you will already know how to pixel control/map such fixtures but here is a list of the software I would recommend:

* [MADRIX](https://madrix.com) (Made specificly for pixel mapping/control.)
* [Resolume Arena](https://resolume.com) (Originally made for visual playback but you can output DMX to such pixel fixtures and map you visuals to them.)
* [grandMA3](https://malighting.com/grandma3/) (If you already spend all your money on that sweet little onPC node it is still a good solution. I mean the selection grid is a good way to map the pixels as subfixtures)
* [grandMA2](https://malighting.com/product-archive/products/grandma2/) (I personally havn't used grandMA2 because I started with grandMA3 but I think it would also be possible to map the pixels in some do-able way.)
* Software I only heard of but that also should work:
  * [ENTTEC LED MAPPER](https://enttec.com/product/dmx-lighting-control-software/pixel-mapping-software/) (ELM)
  * [PIXXEM](https://chromateq.com/pixxem/)
  * [MadMapper](https://madmapper.com)
  * [Touchdesigner](https://derivative.ca)

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
  * Another MicroSD card (minimum 8GB)
  * Small powerbank (idk just look for something that fits your usage and online time)
  * Raspberry Pi Zero Case (I have the official one)
  * Some wire for soldering the strip
  * And you need a defusor tube for the strip (I am still looking for one so if I find one I am going to also put a link here)

## Now the software installation part:

### PiXelTube Master (PXM) for me it's is a Raspberry Pi 4 as I already mentioned:

* Download the Raspberry Pi Imager [here](https://www.raspberrypi.com/software/).
* Plug the MicroSD card for your PXM into your computer.
* Click "Choose model" > "No filtering".
* Click "Choose OS" > "Raspberry Pi OS (other)" > Raspberry Pi OS (Legacy, 64-bit) Lite.
* Click "Select SD card" and select the SD card you want to install the OS to. **Be carefull** if you acidentially select the wrong drive (e.g. your important USB drive with goverment confidential document on) **all data on it will be earesed**** because it will be formated in order to install the OS.
* Click "Next" > "Edit settings".
* Input a hostname (e.g. "pxm"), a username and password (pxm and a password that you can remember or that you've written down somewhere) and **don't** set-up a wifi, because the software is using the wifi module.
* Go to the tab "Services" > "Enable SSH".
* Now click on "Save" > "Yes" > "Yes" and now you can sit back and wait while the imager is installing the operating system on the MicroSD card.
* When the imager is done, plug in the MicroSD card into the Raspberry Pi via the MicroSD slot.
* Before plugging in the powersupply connect the Pi via a Ethernet cable router.
* Now plug in the power and go to the webpage of your router. From there go into the list of all devices that are online. This is router/manufacturer specific, so if you don't know how to do it take a look in the manual for the router online or as in the manual that was in the box with the router.
* After 30 seconds to 2 minutes you should see your Pi with the hostname you gave it.
* The Pi should have an IP address. Copy it or write it down.
* Now open a terminal on your computer.
  * Windows: Press the windows key on your keyboard and type the word "cmd" and hit enter.
  * MAC: Press "command"+"space" and type "terminal" and hit enter.
  * Linux: Hey, I know that you as a linux user already know how to do this, so I don't need to explain how to do this ;)
* Now in the terminal type the following command: `ssh <username you set for the pi>@<ip address of the pi>`
* A promt should appear to enter a password. Just enter the password you set for the PI.
* Now comes the fun part of just copy pasta ;)

### Commands to install all the required packages:

```
sudo apt update -y && sudo apt upgrade -y && sudo apt install python3 python3-pip git python3-flask apache2 php mariadb-server mariadb-client ola ola-python dnsmasq hostapd rfkill mosquitto mosquitto-clients python3-mysqldb -y
pip3 install Flask
pip3 install Requests
pip3 install python-artnet
pip3 install wifi
pip3 install paho-mqtt
pip3 install get-mac
pip3 install netifaces
```

### Setup the wifi access point:

This is required for the tubes to connect to the master server. The tubes will connect over wifi to the master server to receive their configurations and their ArtNET.

Copy and paste the following commands:

Stop the access point (ap) services and unlokc wlan0:

```
sudo systemctl stop dnsmasq
sudo systemctl stop hostapd
rfkill unblock wlan
```

Set static IP for wifi interface:

```
sudo nano /etc/dhcpcd.conf
```

Past this into the text editor (nano) at the very end of the file:

```
interface wlan0
    static ip_address=192.168.0.1/24
    nohook wpa_supplicant
```

This ^ gives the Raspberry Pi on the Wifi interface the IP 192.168.0.1

Tip: If you can't connect over ethernet to the Pi or you want to give it a static ip on the ethernet interface later, just connect to the wifi and you can acccess it via this ip on ssh and all the webinterfaces.

Exit and save nano by pressing [Ctrl]+[O] then [Enter] and then [Ctrl]+[x]. Keep this in mind for later.

Configure DHCP:

Edit the DHCP config:

```
sudo mv /etc/dnsmasq.conf /etc/dnsmasq.conf.orig
sudo nano /etc/dnsmasq.conf
```

Again, past this into nano:

```
interface=wlan0
dhcp-range=192.168.0.2,192.168.0.254,255.255.255.0,24h
```

Now exit nano again. Do you remember how? If not here is how you do it ;)

Exit and save nano by pressing [Ctrl]+[O] then [Enter] and then [Ctrl]+[x].

Now start the DHCP service:

```
sudo systemctl start dnsmasq
```

Configure the AP itself:

Edit the config:

```
sudo nano /etc/hostapd/hostapd.conf
```

Past this:

```
country_code=DE
interface=wlan0
ssid=PiXelTube
channel=13
auth_algs=1
wpa=2
wpa_passphrase=change_me
wpa_key_mgmt=WPA-PSK
rsn_pairwise=CCMP
macaddr_acl=0
```

ATTENTION: for the country_code set your own and also change the wpa_passphrase to a password you remember or wrote down. This password is important for later. With this every tube can connect to the AP.

Exit and save.

Now edit the hostapd file:

```
sudo nano /etc/default/hostapd
```

Find the line with `#DAEMON_CONF` and replace it with this:

```
DAEMON_CONF="/etc/hostapd/hostapd.conf"
```

Exit and save.

Now set your Wifi country code for the interface:

`sudo raspi-config` > "Localisation Options" > "WLAN Country" > Select your country code by pressing Enter > "Ok" > "Finish"

Now enable and start all required services and restart:

```
sudo systemctl unmask hostapd
sudo systemctl enable hostapd
sudo systemctl start hostapd
```

### Setup the MySQL database:

```
sudo mysql -u root -p

# At the password prompt, just hit enter. We are going to change the root password in a second

alter user root@localhost identified by 'a password you write down or remember';

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

exit;

sudo systemctl restart apache2
```

### Setup a MQTT broker for the communication between the master and the tubes:

Enable the service

`sudo systemctl enable mosquitto.service`

Now we are going to enable remote access to the broker.

Edit the config file

`sudo nano /etc/mosquitto/mosquitto.conf`

Paste the following two lines in the config file:

```
listener 1883
allow_anonymous true
```

Now save and exit and restart the services:

`sudo systemctl restart mosquitto`

### Clone the project to your Pi

You can just clone the project itself into your home directory.

`cd ~ && git clone https://github.com/ping-mee/PiXelTubes`

Then just change directory into the server folder.

`cd PiXelTubes/server`

### Installation of the PiXelTube itself

* Plug the MicroSD card for your PXT into your computer.
* Click "Choose model" > "No filtering".
* Click "Choose OS" > "Raspberry Pi OS (other)" > Raspberry Pi OS (Legacy, 32-bit) Lite.
* Click "Select SD card" and select the SD card you want to install the OS to. **Be carefull** if you acidentially select the wrong drive (e.g. your important USB drive with goverment confidential document on) **all data on it will be earesed**** because it will be formated in order to install the OS.
* Click "Next" > "Edit settings".
* Input a hostname that is unique to this specific tube later in the process (e.g. "PiXelTube-1"), a username and password (pxm and a password that you can remember or that you've written down somewhere).
* Click "Setup wifi" and input the SSID and password you've set when you installed the wifi access point in the PXM installation. Also set the wifi country to the country you also set for your wifi ap.
* Go to the tab "Services" > "Enable SSH".
* Now click on "Save" > "Yes" > "Yes" and now you can sit back and wait while the imager is installing the operating system on the MicroSD card.
* When the imager is done, plug in the MicroSD card into the Raspberry Pi via the MicroSD slot.
* Before plugging in the powersupply connect the Pi via a Ethernet cable router.
* Now plug in the power.
* Wait around a minute and then log into your PiXelMaster via SSH.
* Enter the following comment: `cat /var/lib/misc/dnsmasq.leases`.
* If you have set up the wifi correctly, the Tube with it's unique hostname will show up. There should be an IP address. Copy it or write it down.
* Now open a terminal on your computer.
  * Windows: Press the windows key on your keyboard and type the word "cmd" and hit enter.
  * MAC: Press "command"+"space" and type "terminal" and hit enter.
  * Linux: Hey, I know that you as a linux user already know how to do this, so I don't need to explain how to do this ;)
* Now in the terminal type the following command: `ssh <username you set for the pi>@<ip address of the pi>`
* A promt should appear to enter a password. Just enter the password you set for the Pi.

### Commands to install all the required packages:

```
sudo apt update -y && sudo apt upgrade -y && sudo apt install python3 python3-pip git -y
pip3 install adafruit_circuitpython_neopixel
pip3 install Requests
pip3 install wifi
pip3 install paho-mqtt
pip3 install get-mac
```

### Clone the project to your Pi

You can just clone the project itself into your home directory.

`cd ~ && git clone https://github.com/ping-mee/PiXelTubes`

Then just change directory into the client folder.

`cd PiXelTubes/client`
