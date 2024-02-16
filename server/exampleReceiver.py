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

### ArtNet Config ###
artnetBindIp = str(get_eth0_ip())
# artnetBindIp = "10.0.0.4"
artnetUniverse = 0

### Art-Net Setup ###
# Sets debug in Art-Net module.
# Creates Artnet socket on the selected IP and Port
artNet = Artnet.Artnet(artnetBindIp, DEBUG=debug)

while True:
    try:
        # Gets whatever the last Art-Net packet we received is
        artNetPacket = artNet.readPacket()
        print(artNetPacket)
        
    except KeyboardInterrupt:
        break
    except Exception as e:
        print(e)

# Close the various connections cleanly so nothing explodes :)
artNet.close()
sys.exit()