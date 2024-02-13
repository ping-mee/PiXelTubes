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
#     return "10.0.0.4"

# What DMX channels we want to listen to
dmxChannels = 512

### ArtNet Config ###
artnetBindIp = get_eth0_ip()
artnetUniverse = 1

### Art-Net Setup ###
# Sets debug in Art-Net module.
# Creates Artnet socket on the selected IP and Port
artNet = Artnet.Artnet(BINDIP = artnetBindIp, DEBUG = False, SHORTNAME = "PiXelTubeMaster", LONGNAME = "PiXelTubeMaster", PORT = 6454)

tuple_ip = (str(get_eth0_ip()), 6454)
while True:
    try:
        # Gets whatever the last Art-Net packet we received is
        artNetPacket = artNet.readPacket()
        # Make sure we actually *have* a packet
        if artNetPacket is not None and artNetPacket.data is not None:
            print("Packet: "+str(artNetPacket))
            print("Universe: "+str(artNetPacket.universe))
            print("Data: "+str(artNetPacket.data))
            print(" ")
            # Checks to see if the current packet is for the specified DMX Universe
            if artNetPacket.universe == artnetUniverse:
                # Stores the packet data array
                dmxPacket = artNetPacket.data
                
                # Then print out the data from each channel
                print("Received data: ", end="")
                for i in range(dmxChannels):
                    # Lists in python start at 0, so to access a specific DMX channel you have to subtract one
                    print(dmxPacket[i-1], end=" ")
                
                # Print a newline so things look nice :)
                print("")
        else:
            print("Artnet packet was None. I hate everything, I hate my life, myself and my coding skills. What am I doing. I don't know... BTW, fuck Artnet for being such a shitty protocol.")
        
    except KeyboardInterrupt:
        break

# Close the various connections cleanly so nothing explodes :)
artNet.close()
sys.exit()