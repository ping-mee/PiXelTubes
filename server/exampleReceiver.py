import time
import sys
import python_artnet as Artnet
import os

artnet = Artnet.Artnet()


while True:
    try:
        
        artNetPacket = artnet.readPacket()
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