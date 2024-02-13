import time
import sys
import python_artnet as Artnet
import netifaces

def get_eth0_ip():
    try:
        # Get the IP address of the eth0 interface
        eth0_ip = netifaces.ifaddresses('eth0')[netifaces.AF_INET][0]['addr']
        return str(eth0_ip)
    except (KeyError, IndexError, OSError) as e:
        print(f"Error getting eth0 IP: {e}")
        return None

debug = True

# What DMX channels we want to listen to
dmxChannels = [1,2,3,4,5,6]

### ArtNet Config ###
print(str(get_eth0_ip()))
artnetBindIp = str(get_eth0_ip)
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
                # Stores the packet data array
                dmxPacket = artNetPacket.data
                
                # Then print out the data from each channel
                print("Received data: ", end="")
                for i in dmxChannels:
                    # Lists in python start at 0, so to access a specific DMX channel you have to subtract one
                    print(dmxPacket[i-1], end=" ")
                
                # Print a newline so things look nice :)
                print("")
                
        time.sleep(0.1)
        
    except KeyboardInterrupt:
        break

# Close the various connections cleanly so nothing explodes :)
artNet.close()
sys.exit()