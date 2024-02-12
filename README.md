# PiXelTubes

### A little introduction :)

PiXelTubes is a little fun project for me. **(CURRENTLY WORK IN PROGRESS)**

It is inspired by the Astera Helios/Titan tubes. The most classic, state of the art LED tubes for event lighting.

So maybe the question comes up, why I don't just buy some of them and use them. For me a big problem is the price and also I wanted a little project for my holiday week. So I thought why not build a cheap alternative with some led strips and some Raspberry Pi's.

BTW excuse the very "creative" name, but every Raspberry Pi project has to have a "Pi" in it's name.

For this project you will need a soldering iron and atleast a bit of knowledge on how to solder because you will have to solder the strip to the Raspberry Pi Zero.

### Before we start with what you need to build your own PiXelTube system here are some ideas on how to integrate those PiXelTubes.

**DISCLAIMER:** I am not sponsored by an company/software I am mentioning. These are just recommendations ;)

For the beginners or "newbies" to lighting you can use free solutions like QLC+ for a small setup. Only problem with QLC+ is that pixel control is a bit complex.

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
* Click "Choose OS" > "Raspberry Pi OS (other)" > Raspberry Pi OS Lite (64-bit).
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
sudo apt install python3 python3-pip git python3-flask apache2 php mariadb-server mariadb-client ola ola-python dnsmasq hostapd -y

pip3 install flask-mysqldb
pip3 install adafruit-circuitpython-neopixel
pip3 install wifi
```

### Setup the wifi access point:

This is required for the tubes to connect to the master server. The tubes will connect over wifi to the master server to receive their configurations and their ArtNET.

Copy and paste the following commands:

Stop the access point (ap) services:

```
sudo systemctl stop dnsmasq
sudo systemctl stop hostapd
```

Set static IP for wifi interface:

```
sudo nano /etc/dhcpcd.conf
```

Past this into the text editor (nano):

```
interface wlan0
    static ip_address=192.168.0.1/24
    nohook wpa_supplicant
```

This ^ gives the Raspberry Pi on the Wifi interface the IP 192.168.0.1

Tip: If you can't connect over ethernet to the Pi or you want to give it a static ip on the ethernet interface later, just connect to the wifi and you can acccess it via this ip on ssh and all the webinterfaces.

Exit and save nano by pressing [Cntrl]+[O] then [Enter] and then [Cntrl]+[x]. Keep this in mind for later.

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

Exit and save nano by pressing [Cntrl]+[O] then [Enter] and then [Cntrl]+[x].

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

Now enable and start all required services and restart:

```
sudo systemctl unmask hostapd
sudo systemctl enable hostapd
sudo systemctl start hostapd
sudo reboot
```

### Setup the MySQL database:

```
sudo mysql -u root -p

# Enter the password you set for the pi

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
```

<style>#mermaid-1707698043143{font-family:"trebuchet ms",verdana,arial;font-size:16px;fill:#ccc;}#mermaid-1707698043143 .error-icon{fill:#a44141;}#mermaid-1707698043143 .error-text{fill:#ddd;stroke:#ddd;}#mermaid-1707698043143 .edge-thickness-normal{stroke-width:2px;}#mermaid-1707698043143 .edge-thickness-thick{stroke-width:3.5px;}#mermaid-1707698043143 .edge-pattern-solid{stroke-dasharray:0;}#mermaid-1707698043143 .edge-pattern-dashed{stroke-dasharray:3;}#mermaid-1707698043143 .edge-pattern-dotted{stroke-dasharray:2;}#mermaid-1707698043143 .marker{fill:lightgrey;}#mermaid-1707698043143 .marker.cross{stroke:lightgrey;}#mermaid-1707698043143 svg{font-family:"trebuchet ms",verdana,arial;font-size:16px;}#mermaid-1707698043143 .label{font-family:"trebuchet ms",verdana,arial;color:#ccc;}#mermaid-1707698043143 .label text{fill:#ccc;}#mermaid-1707698043143 .node rect,#mermaid-1707698043143 .node circle,#mermaid-1707698043143 .node ellipse,#mermaid-1707698043143 .node polygon,#mermaid-1707698043143 .node path{fill:#1f2020;stroke:#81B1DB;stroke-width:1px;}#mermaid-1707698043143 .node .label{text-align:center;}#mermaid-1707698043143 .node.clickable{cursor:pointer;}#mermaid-1707698043143 .arrowheadPath{fill:lightgrey;}#mermaid-1707698043143 .edgePath .path{stroke:lightgrey;stroke-width:1.5px;}#mermaid-1707698043143 .flowchart-link{stroke:lightgrey;fill:none;}#mermaid-1707698043143 .edgeLabel{background-color:hsl(0,0%,34.4117647059%);text-align:center;}#mermaid-1707698043143 .edgeLabel rect{opacity:0.5;background-color:hsl(0,0%,34.4117647059%);fill:hsl(0,0%,34.4117647059%);}#mermaid-1707698043143 .cluster rect{fill:hsl(180,1.5873015873%,28.3529411765%);stroke:rgba(255,255,255,0.25);stroke-width:1px;}#mermaid-1707698043143 .cluster text{fill:#F9FFFE;}#mermaid-1707698043143 div.mermaidTooltip{position:absolute;text-align:center;max-width:200px;padding:2px;font-family:"trebuchet ms",verdana,arial;font-size:12px;background:hsl(20,1.5873015873%,12.3529411765%);border:1px solid rgba(255,255,255,0.25);border-radius:2px;pointer-events:none;z-index:100;}#mermaid-1707698043143:root{--mermaid-font-family:sans-serif;}#mermaid-1707698043143:root{--mermaid-alt-font-family:sans-serif;}#mermaid-1707698043143 flowchart{fill:apa;}</style>

### Setup Open Lighting Archetecture as the ArtNET sACN middle man:

You can access the Pi's OLA webinterface via the following address:

`http://<ip_of_the_pi>:9090/`

* From there click add universe > set universe ID > set universe name.
* Select Artnet input with the IP address from the ethernet port and as Artnet output the address from the wifi access point.

Repeat this process for every universe you are going to use for your tubes. As an addition to Artnet you can also use sACN (E1.31) as an input.
