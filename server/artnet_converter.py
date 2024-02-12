import socket

def forward_artnet(iface_in, iface_out):
    # Create raw socket to receive and send ArtNet packets
    sock_in = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(0x0003))
    sock_in.bind((iface_in, 0))

    sock_out = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(0x0003))
    sock_out.bind((iface_out, 0))

    while True:
        # Receive ArtNet packet from the input interface
        pkt, _ = sock_in.recvfrom(65535)

        # Modify the source MAC address if needed
        # Modify other fields as required

        # Forward the packet to the output interface
        sock_out.sendall(pkt)

        print(f"Forwarded ArtNet packet from {iface_in} to {iface_out}")

# Specify the input and output interfaces
input_interface = "eth0"
output_interface = "wlan0"

# Start forwarding ArtNet packets between interfaces
forward_artnet(input_interface, output_interface)
