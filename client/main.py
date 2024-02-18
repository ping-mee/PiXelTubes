import subprocess
import neopixel
import requests
import time
import paho.mqtt.client as mqtt
from getmac import get_mac_address
import board

SERVER_IP = '192.168.0.1'
SERVER_PORT = 5000
wlan_mac_address = str(get_mac_address(interface="wlan0"))
LED_STRIP_PIN = board.D18
LED_COUNT = 30
LEDS_PER_PIXEL = 5
strip = neopixel.NeoPixel(pin=LED_STRIP_PIN, n=LED_COUNT, auto_write=True)

def on_message(mqttc, obj, msg):
    global rgb_values_list
    rgb_values_list = [tuple(map(int, color.strip('[]').split(', '))) for color in msg.payload.decode().strip('[]').split('], [')]

def update_led_strip(rgb_values_list, strip):
    for i, rgb_values in enumerate(rgb_values_list):
        for pixel in range(i * LEDS_PER_PIXEL, (i + 1) * LEDS_PER_PIXEL):
            strip[pixel] = rgb_values

if __name__ == "__main__":
    # Connect to Wi-Fi and other setup code...

    mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    # MQTT setup code...
    mqttc.on_message = on_message

    mqttc.loop_start()
    while True:
        update_led_strip(rgb_values_list, strip)
        time.sleep(0.5)
