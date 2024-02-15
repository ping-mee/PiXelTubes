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

### ArtNet Config ###
artnetBindIp = get_eth0_ip()

### Art-Net Setup ###
# Sets debug in Art-Net module.
# Creates Artnet socket on the selected IP and Port
artNet = Artnet.Artnet(BINDIP = artnetBindIp, DEBUG = False, SHORTNAME = "PiXelTubeMaster", LONGNAME = "PiXelTubeMaster", PORT = 6454)
tuple_ip = (str(get_eth0_ip()), 6454)
# artNet.art_pol_reply(tuple_ip)
while True:
    try:
        # Gets whatever the last Art-Net packet we received is
        artNetPacket = artNet.readPacket()
        # Make sure we actually *have* a packet
        if artNetPacket is not None and artNetPacket.data is not None:
            if artNetPacket.universe == 0:
                print("YES")
            else:
                print("Universe: "+str(artNetPacket.universe))
            # Stores the packet data array
            # dmxPacket = artNetPacket.data
        
    except KeyboardInterrupt:
        break

# Close the various connections cleanly so nothing explodes :)
artNet.close()
sys.exit()