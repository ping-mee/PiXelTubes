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
import sys
import ast

SERVER_IP = '192.168.0.1'
SERVER_PORT = 5000

# Dynamically obtain the MAC address of the WLAN interface
wlan_mac_address = str(get_mac_address(interface="wlan0"))

# Replace with the GPIO pin connected to the data input of the WS2812B LED strip
LED_STRIP_PIN = board.D18
global LED_COUNT
LED_COUNT = 30
global LEDS_PER_PIXEL
LEDS_PER_PIXEL = 5

# Global variables for LED strip control
global strip
strip = neopixel.NeoPixel(pin = board.D18, n = LED_COUNT, auto_write = True, pixel_order = neopixel.RGB)

def register_tube():
    # Register or reauthenticate the tube with the server
    try:
        response = requests.post(f'http://{SERVER_IP}:{SERVER_PORT}/register_tube', data={'mac_address': wlan_mac_address})
        print(response)
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
    output = subprocess.check_output(['iwgetid']).decode()
    return output.split('"')[1]
    
def update_led_strip(rgb_values, pixel, strip):
    strip[int(pixel)] = rgb_values

def on_message(mqttc, obj, msg):
    rgb_values_list = msg.payload.decode()
    print(rgb_values_list)

    # for pixel in range(LEDS_PER_PIXEL):
    #     update_led_strip(rgb_values, pixel, strip)

    # for pixel in range(LEDS_PER_PIXEL, LEDS_PER_PIXEL*2):
    #     update_led_strip(rgb_values, pixel, strip)

    # for pixel in range(LEDS_PER_PIXEL*2, LEDS_PER_PIXEL*3):
    #     update_led_strip(rgb_values, pixel, strip)

    # for pixel in range(LEDS_PER_PIXEL*3, LEDS_PER_PIXEL*4):
    #     update_led_strip(rgb_values, pixel, strip)

    # for pixel in range(LEDS_PER_PIXEL*4, LEDS_PER_PIXEL*5):
    #     update_led_strip(rgb_values, pixel, strip)

    # for pixel in range(LEDS_PER_PIXEL*5, LEDS_PER_PIXEL*6):
    #     update_led_strip(rgb_values, pixel, strip)

if __name__ == "__main__":
    # Connect to Wi-Fi
    if is_connected_to_wifi() is not None:
        # Register/reauthenticate the tube
        register_tube()
        time.sleep(1)

        mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        mqttc.connect("192.168.0.1", 1883, 60)
        mqttc.on_message = on_message
        mqttc.subscribe("tube-"+str(wlan_mac_address)+"/pixel_colors", 0)

        mqttc.loop_forever()