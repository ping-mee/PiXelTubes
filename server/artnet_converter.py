from scapy.all import *
from scapy.arch import get_if_addr

def forward_artnet(pkt):
    # Check if the packet is an ArtNet packet
    if pkt.haslayer(IP) and pkt.haslayer(UDP) and pkt[UDP].dport == 6454:
        # Check the source IP address and interface
        if pkt[IP].src.startswith("10.0.") and pkt.route()[0] == "eth0":
            # Modify the source IP address to the new network
            pkt[IP].src = get_if_addr("wlan0")
            # Forward the packet to the new network
            send(pkt, iface="wlan0")
            print("Forwarded ArtNet packet from eth0 to wlan0")

# Sniff ArtNet packets on eth0
while True:
    sniff(iface="eth0", prn=forward_artnet, store=0)