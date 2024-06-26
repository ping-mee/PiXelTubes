import subprocess
import neopixel
import requests
import time
import paho.mqtt.client as mqtt
from getmac import get_mac_address
import board

# var's for web api server. Change them if you use another IP scheme for the DHCP.
SERVER_IP = '192.168.0.1'
SERVER_PORT = 5000

# get the current MAC address from the wlan0 interface to use it as the unique id in the DB
wlan_mac_address = str(get_mac_address(interface="wlan0"))

# var's for pin and led count to use them in the neopixel module
LED_STRIP_PIN = board.D18
global LED_COUNT
LED_COUNT = 30

# global variables for LED strip control
global strip
strip = neopixel.NeoPixel(pin = board.D18, n = LED_COUNT, auto_write = True)

def register_tube():
    # register or reauthenticate the tube with the server
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
    # request the own settings via the unique ID
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
    # check via subprocess command if you wifi is connected to the AP
    output = subprocess.check_output(['iwgetid']).decode()
    return output.split('"')[1]
    
def update_led_strip(rgb_values, pixel, strip):
    # set retraived RGB values to the spicified pixel
    strip[int(pixel)] = rgb_values

def on_message(mqttc, obj, msg):
    # get the rgb value list on new mqtt message from the subscribed topic
    global rgb_values_list
    rgb_values_list = eval(msg.payload.decode())

if __name__ == "__main__":
    # run wifi connection check
    if is_connected_to_wifi() is not None:
        # if connected successfully run registration/reauthentication process
        register_tube()
        time.sleep(1)
        
        # open MQTT client
        mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        mqttc.connect("192.168.0.1", 1883, 60)
        mqttc.on_message = on_message
        mqttc.subscribe("tube-"+str(wlan_mac_address)+"/pixel_colors", 0)

        # create a default rgb value list to get a black output
        global rgb_values_list
        rgb_values_list = eval("['[0, 0, 0]', '[0, 0, 0]', '[0, 0, 0]', '[0, 0, 0]', '[0, 0, 0]', '[0, 0, 0]']")

        # start MQTT server in background loop
        mqttc.loop_start()
        while True:
            # try updating the single pixels
            try:
                for pixel in range(5):
                    update_led_strip(tuple(eval(rgb_values_list[0])), pixel, strip)

                for pixel in range(5, 10):
                    update_led_strip(tuple(eval(rgb_values_list[1])), pixel, strip)

                for pixel in range(10, 15):
                    update_led_strip(tuple(eval(rgb_values_list[2])), pixel, strip)

                for pixel in range(15, 20):
                    update_led_strip(tuple(eval(rgb_values_list[3])), pixel, strip)

                for pixel in range(20, 25):
                    update_led_strip(tuple(eval(rgb_values_list[4])), pixel, strip)

                for pixel in range(25, 30):
                    update_led_strip(tuple(eval(rgb_values_list[5])), pixel, strip)
            except KeyboardInterrupt:
                # if code stop via cntrl+c blackout
                for led in range(LED_COUNT):
                    update_led_strip((0, 0, 0), led, strip)