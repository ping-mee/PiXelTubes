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

# def get_eth0_ip():
#     return "10.0.0.150"

debug = True

# What DMX channels we want to listen to
dmxChannels = 512

### ArtNet Config ###
artnetBindIp = get_eth0_ip()
artnetUniverse = 0

### Art-Net Setup ###
# Sets debug in Art-Net module.
# Creates Artnet socket on the selected IP and Port
artNet = Artnet.Artnet(BINDIP = artnetBindIp, SYSIP=artnetBindIp, DEBUG = True, SHORTNAME = "PiXelTubeMaster", LONGNAME = "PiXelTubeMaster", PORT = 6454)

tuple_ip = (str(get_eth0_ip()), 6454)
while True:
    try:
        artNet.art_pol_reply(tuple_ip)
        # Gets whatever the last Art-Net packet we received is
        artNetPacket = artNet.readPacket()
        print("Packet: "+str(artNetPacket))
        print("Universe: "+str(artNetPacket.universe))
        print("Data: "+str(artNetPacket.data))
        print(" ")
        # Make sure we actually *have* a packet
        if artNetPacket is not None and artNetPacket.data is not None:
            # Checks to see if the current packet is for the specified DMX Universe
            if artNetPacket.universe == artnetUniverse:
                # Stores the packet data array
                dmxPacket = artNetPacket.data
                
                # Then print out the data from each channel
                print("Received data: ", end="")
                for i in len(dmxChannels):
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