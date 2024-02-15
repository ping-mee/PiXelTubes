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

debug = True

### ArtNet Config ###
artnetBindIp = str(get_eth0_ip())
artnetUniverse = 0

### Art-Net Setup ###
# Sets debug in Art-Net module.
# Creates Artnet socket on the selected IP and Port
artNet = Artnet.Artnet(artnetBindIp, DEBUG=debug)

while True:
    try:
        # Gets whatever the last Art-Net packet we received is
        artNetPacket = artNet.readPacket()
        # Make sure we actually *have* a packet
        if artNetPacket is not None and artNetPacket.data is not None:
            # Checks to see if the current packet is for the specified DMX Universe
            if artNetPacket.universe == artnetUniverse:
                print("Received specified universe: "+str(artNetPacket.universe))
                
                # Print a newline so things look nice :)
            else:
                print("Did not receive specified universe. The received universe was universe: "+str(artNetPacket.universe))
                
        time.sleep(0.1)
        
    except KeyboardInterrupt:
        break

# Close the various connections cleanly so nothing explodes :)
artNet.close()
sys.exit()