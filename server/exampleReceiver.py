import time
import sys
import python_artnet as Artnet
import os

def get_eth0_ip():
    try:
        # Get the IP address of the eth0 interface
        eth0_ip = str(os.system("ip -4 -o addr show eth0 | awk '{print $4}' | cut -d '/' -f 1 "))
        return eth0_ip
    except (KeyError, IndexError, OSError) as e:
        print(f"Error getting eth0 IP: {e}")
        exit

debug = False

# You can choose between setting your own IP or if you run this on a Pi getting a IP automatically form eth0
# artnetBindIp = str(get_eth0_ip())
artnetBindIp = "10.0.0.4"

artnetUniverse = 0

### Art-Net Setup ###
# Creates Artnet socket on the selected IP and Port
artNet = Artnet.Artnet(artnetBindIp, DEBUG=debug)

while True:
    try:
        # Read latest ArtNet packet
        artNetPacket = artNet.readBuffer()[artnetUniverse]
        # Print out the universe of said packet
        print("My univ: "+str(artNetPacket.data))
    
    # Big red stop button just in case
    except KeyboardInterrupt:
        break
    # Give me that exceptions
    except Exception as e:
        print(e)
    # Slow down there young fella
    time.sleep(0.1)

# Bro, close dat shit! It is over for today! No more Mario Kart 8 Deluxe
artNet.close()
sys.exit()