import socket
import os
import wifi
from pythonosc import udp_client
from neopixel import *
import threading
import requests
import json

# Replace with your server's IP address and port
SERVER_IP = '192.168.0.1'  # Change to the actual IP of the PiXelTube Master
SERVER_PORT = 5000  # Change to the port your Flask app is running on

# Dynamically obtain the MAC address of the WLAN interface
wlan_mac_address = ':'.join(['{:02x}'.format((int(os.popen(f'cat /sys/class/net/wlan0/address').read().split(':'))[i]),) for i in range(6)])

# Replace with the GPIO pin connected to the data input of the WS2812B LED strip
LED_STRIP_PIN = 18
LED_COUNT = 60

# Global variables for LED strip control
strip = Adafruit_NeoPixel(LED_COUNT, LED_STRIP_PIN, 800000, 10, False)
strip.begin()

def register_tube():
    # Register or reauthenticate the tube with the server
    try:
        response = requests.post(f'http://{SERVER_IP}:{SERVER_PORT}/register_tube', data={'mac_address': wlan_mac_address})
        data = response.json()
        if data.get('success'):
            print('Tube registered successfully.')
        else:
            print(f'Registration failed: {data.get("message")}')
    except requests.RequestException as e:
        print(f'Registration failed: {e}')

def is_connected_to_wifi():
    try:
        ssid = wifi.current()
        return ssid is not None
    except wifi.exceptions.InterfaceError:
        return False

def listen_to_artnet(universe, dmx_address):
    # Set up Art-Net client
    client = udp_client.SimpleUDPClient(SERVER_IP, SERVER_PORT)

    # Listen to Art-Net messages
    while True:
        try:
            # Receive Art-Net message
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
                sock.bind(('0.0.0.0', 6454))  # Listen on all interfaces
                data, addr = sock.recvfrom(1024)

            # Process Art-Net message
            universe_id = int.from_bytes(data[14:15], byteorder='big')
            dmx_start_address = int.from_bytes(data[15:17], byteorder='big')

            if universe_id == universe and dmx_start_address <= dmx_address <= dmx_start_address + 2 * LED_COUNT:
                # Extract RGB values from Art-Net packet
                r = data[17]
                g = data[18]
                b = data[19]

                # Map DMX address to LED index
                led_index = (dmx_address - dmx_start_address) // 3

                # Update LED strip
                strip.setPixelColor(led_index, Color(r, g, b))
                strip.show()

                # Send confirmation to the server
                client.send_message('/acknowledge', {'tube_id': wlan_mac_address, 'led_index': led_index})

        except Exception as e:
            print(f"Error: {e}")

def get_assigned_params():
    try:
        response = requests.get(f'http://{SERVER_IP}:{SERVER_PORT}/get_assigned_params/{wlan_mac_address}')
        data = response.json()
        if data.get('success'):
            return data.get('universe'), data.get('dmx_address')
        else:
            print(f'Failed to fetch assigned parameters: {data.get("message")}')
            return None, None
    except requests.RequestException as e:
        print(f'Failed to fetch assigned parameters: {e}')
        return None, None

if __name__ == "__main__":
    # Connect to Wi-Fi
    if is_connected_to_wifi():
        # Register/reauthenticate the tube
        register_tube()

        # Fetch assigned universe and DMX address
        assigned_universe, assigned_dmx_address = get_assigned_params()

        if assigned_universe is not None and assigned_dmx_address is not None:
            # Start a thread for listening to Art-Net messages
            art_net_thread = threading.Thread(target=listen_to_artnet, args=(assigned_universe, assigned_dmx_address))
            art_net_thread.start()

            # Wait for the thread to finish (you can add more logic here as needed)
            art_net_thread.join()
