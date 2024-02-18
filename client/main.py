_D='message'
_C='success'
_B='192.168.0.1'
_A=None
import subprocess,neopixel,requests,time,paho.mqtt.client as mqtt
from getmac import get_mac_address
import board
SERVER_IP=_B
SERVER_PORT=5000
wlan_mac_address=str(get_mac_address(interface='wlan0'))
LED_STRIP_PIN=board.D18
global LED_COUNT
LED_COUNT=30
global LEDS_PER_PIXEL
LEDS_PER_PIXEL=5
global strip
strip=neopixel.NeoPixel(pin=board.D18,n=LED_COUNT,auto_write=True)
def register_tube():
	try:
		response=requests.post(f"http://{SERVER_IP}:{SERVER_PORT}/register_tube",data={'mac_address':wlan_mac_address});print(response);data=response.json()
		if data.get(_C):print('Tube registered successfully.')
		else:print(f"Registration failed: {data.get(_D)}")
	except requests.RequestException as e:print(f"Registration failed: {e}")
def get_assigned_params():
	try:
		response=requests.get(f"http://{SERVER_IP}:{SERVER_PORT}/get_assigned_params/{wlan_mac_address}");data=response.json()
		if data.get(_C):return data.get('universe'),data.get('dmx_address')
		else:print(f"Failed to fetch assigned parameters: {data.get(_D)}");return _A,_A
	except requests.RequestException as e:print(f"Failed to fetch assigned parameters: {e}");return _A,_A
def is_connected_to_wifi():output=subprocess.check_output(['iwgetid']).decode();return output.split('"')[1]
def update_led_strip(rgb_values,pixel,strip):strip[int(pixel)]=rgb_values
def on_message(mqttc,obj,msg):global rgb_values_list;rgb_values_list=eval(msg.payload.decode())
if __name__=='__main__':
	if is_connected_to_wifi()is not _A:
		register_tube();time.sleep(1);mqttc=mqtt.Client(mqtt.CallbackAPIVersion.VERSION2);mqttc.connect(_B,1883,60);mqttc.on_message=on_message;mqttc.subscribe('tube-'+str(wlan_mac_address)+'/pixel_colors',0);global rgb_values_list;rgb_values_list=eval("['[0, 0, 0]', '[0, 0, 0]', '[0, 0, 0]', '[0, 0, 0]', '[0, 0, 0]', '[0, 0, 0]']");mqttc.loop_start()
		while True:
			for pixel in range(LEDS_PER_PIXEL):update_led_strip(tuple(eval(rgb_values_list[0])),pixel,strip)
			for pixel in range(LEDS_PER_PIXEL,LEDS_PER_PIXEL*2):update_led_strip(tuple(eval(rgb_values_list[1])),pixel,strip)
			for pixel in range(LEDS_PER_PIXEL*2,LEDS_PER_PIXEL*3):update_led_strip(tuple(eval(rgb_values_list[2])),pixel,strip)
			for pixel in range(LEDS_PER_PIXEL*3,LEDS_PER_PIXEL*4):update_led_strip(tuple(eval(rgb_values_list[3])),pixel,strip)
			for pixel in range(LEDS_PER_PIXEL*4,LEDS_PER_PIXEL*5):update_led_strip(tuple(eval(rgb_values_list[4])),pixel,strip)
			for pixel in range(LEDS_PER_PIXEL*5,LEDS_PER_PIXEL*6):update_led_strip(tuple(eval(rgb_values_list[5])),pixel,strip)
			time.sleep(.5)