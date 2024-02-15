import time
import sys
import python_artnet as Artnet
import os

artnet = Artnet.Artnet()

def get_eth0_ip():
    try:
        # Get the IP address of the eth0 interface
        eth0_ip = str(os.system("ip -4 -o addr show eth0 | awk '{print $4}' | cut -d '/' -f 1 "))
        return eth0_ip
    except (KeyError, IndexError, OSError) as e:
        print(f"Error getting eth0 IP: {e}")
        exit

while True:
    try:
        
        artNetPacket = artnet.readPacket(BINDIP=get_eth0_ip)
        if artNetPacket is not None and artNetPacket.data is not None:
            if artNetPacket.universe == 0:
                print("Universe was the specified universe: "+str(artNetPacket.universe))
            else:
                print("Universe was not the specified: "+str(artNetPacket.universe))
        else:
            print("Packet was none")
    except KeyboardInterrupt:
        artnet.close()
        break
    time.sleep(0.01)