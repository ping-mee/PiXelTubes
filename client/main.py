import os
import wifi
from sacn import sACNlistener
from neopixel import *
import requests
import json
import time
from threading import Thread

# Replace with your server's IP address and port
SERVER_IP = '192.168.0.1'  # Change to the actual IP of the PiXelTube Master
SERVER_PORT = 5000  # Change to the port your Flask app is running on

# Dynamically obtain the MAC address of the WLAN interface
wlan_mac_address = ':'.join(['{:02x}'.format((int(os.popen(f'cat /sys/class/net/wlan0/address').read().split(':'))[i]),) for i in range(6)])

# Replace with the GPIO pin connected to the data input of the WS2812B LED strip
LED_STRIP_PIN = 18
global LED_COUNT
LED_COUNT = 30
global LEDS_PER_PIXEL
LEDS_PER_PIXEL = 5

# Global variables for LED strip control
global strip
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
    
def is_connected_to_wifi():
    try:
        ssid = wifi.current()
        return ssid is not None
    except wifi.exceptions.InterfaceError:
        return False
    
def update_led_strip(dmx_values, dmx_address, strip, LED_PER_PIXEL):
    for i in range(LED_COUNT):
        pixel_index = i // LEDS_PER_PIXEL
        dmx_index = dmx_address + (pixel_index * 3)

        r = dmx_values[dmx_index]
        g = dmx_values[dmx_index + 1]
        b = dmx_values[dmx_index + 2]

        strip.setPixelColor(i, Color(r, g, b))

    # Update the LED strip
    strip.show()

def listen_to_sacn(universe, dmx_address, strip, LEDS_PER_PIXEL):
    try:
        # Create a new sACN listener
        listener = sACNlistener()

        # Configure the listener to listen to the specified universe
        listener.register_listener(universe)

        # Start the listener
        listener.start()

        while True:
            # Get the latest data from the specified universe
            packet = listener[universe].listen()

            if packet is not None:
                # Extract DMX values from the sACN packet
                dmx_values = packet.dmx_frame

                # Update the LED strip based on the received DMX values
                update_led_strip(dmx_values, dmx_address, strip, LEDS_PER_PIXEL)
    except Exception as e:
        print(f"Error: {e}")

def loopCheckSettingUpdates():
    while True:
        try:
            global universe
            global dmx_address
            universe, dmx_address = get_assigned_params()
        except Exception as e:
            print(f"Error: {e}")
        time.sleep(2)

def loopUpdatePixels():
    while True:
        try:
            listen_to_artnet(universe, dmx_address, strip, LEDS_PER_PIXEL)
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    # Connect to Wi-Fi
    if is_connected_to_wifi():
        # Register/reauthenticate the tube
        register_tube()
        time.sleep(1)
        global universe
        global dmx_address
        universe, dmx_address = get_assigned_params()
        listen_to_artnet(universe, dmx_address, strip, LEDS_PER_PIXEL)

        settingsUpdateThread = Thread(target=loopCheckSettingUpdates, args=())
        pixelUpdateThread = Thread(target=loopUpdatePixels, args=())

        settingsUpdateThread.start()
        pixelUpdateThread.start()