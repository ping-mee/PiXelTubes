import os
import subprocess
import neopixel
import requests
import json
import time
from threading import Thread
import paho.mqtt.client as mqtt
from getmac import get_mac_address
import board

# Replace with your server's IP address and port
SERVER_IP = '192.168.0.1'  # Change to the actual IP of the PiXelTube Master
SERVER_PORT = 5000  # Change to the port your Flask app is running on

# Dynamically obtain the MAC address of the WLAN interface
wlan_mac_address = str(get_mac_address(interface="wlan0"))

# Replace with the GPIO pin connected to the data input of the WS2812B LED strip
LED_STRIP_PIN = board.D18
global LED_COUNT
LED_COUNT = 30
global LEDS_PER_PIXEL
LEDS_PER_PIXEL = 5
global pixel_data
pixel_data = None

# Global variables for LED strip control
global strip
strip = neopixel.NeoPixel(pin = LED_STRIP_PIN, n = LED_COUNT, auto_write = True, pixel_order = neopixel.RGB)

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
    output = subprocess.check_output(['iwgetid'])
    return output.split('"')[1] is not None
    
def update_led_strip(rgb_values, pixel, strip):
        for i in range(LEDS_PER_PIXEL):
            strip[int(pixel)] = Color(rgb_values[i])

def mqtt_listner(msg, universe, dmx_address, strip, LEDS_PER_PIXEL):
    try:
        # Parse the topic to get universe and channel
        _, dmx_universe, channel_number = msg.topic.split("/")
        channel_number = int(channel_number)

        # Calculate the pixel index and channel within the pixel
        pixel_index = (channel_number - dmx_address) // LEDS_PER_PIXEL
        channel_in_pixel = (channel_number - dmx_address) % LEDS_PER_PIXEL

        # Initialize a new pixel entry if not present
        if pixel_index not in pixel_data:
            pixel_data[pixel_index] = [0] * LEDS_PER_PIXEL

        # Update the RGB value for the corresponding channel in the pixel
        pixel_data[pixel_index][channel_in_pixel] = int(msg.payload)

        # Check if all three channels for the pixel are received
        if len(pixel_data[pixel_index]) == LEDS_PER_PIXEL:
            # Set the RGB values for the pixel in the LED strip
            update_led_strip(pixel_index, pixel_data[pixel_index], strip)

            # Remove the pixel entry from the temporary storage
            del pixel_data[pixel_index]

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

def on_message(mqttc, obj, msg):
    mqtt_listner(msg)

if __name__ == "__main__":
    # Connect to Wi-Fi
    if is_connected_to_wifi() is not None:
        # Register/reauthenticate the tube
        register_tube()
        time.sleep(1)
        global universe
        global dmx_address
        universe, dmx_address = get_assigned_params()

        mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        mqttc.connect("192.168.0.1", 1883, 60)
        mqttc.on_message = on_message
        for address in range(dmx_address, dmx_address + 18):
            mqttc.subscribe(str(universe)+"/"+str(address), 0)

        settingsUpdateThread = Thread(target=loopCheckSettingUpdates, args=())
        pixelUpdateThread = Thread(target=mqtt_listner, args=(universe, dmx_address, strip, LEDS_PER_PIXEL))

        settingsUpdateThread.start()
        pixelUpdateThread.start()