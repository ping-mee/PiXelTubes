from flask import Flask, render_template, request, jsonify
import json
import MySQLdb
import paho.mqtt.client as mqtt
import threading
import python_artnet as Artnet
import os
from getmac import get_mac_address

app = Flask(__name__)

wlan_mac_address = str(get_mac_address(interface="wlan0"))

# Read configuration from config.json
try:
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)
except FileNotFoundError:
    # Create config.json with default values if it doesn't exist
    config = {
        "mysql": {
            "host": "localhost",
            "user": "pxm",
            "password": "pixel",
            "database": "pixeltube_db"
        },
        "artnet": {
            "universe_count": 1
        }
    }
    with open('config.json', 'w') as config_file:
        json.dump(config, config_file, indent=4)

database = config['mysql']['database']

db = MySQLdb.connect(
    host=config['mysql']['host'],
    user=config['mysql']['user'],
    password=config['mysql']['password'],
    database=config['mysql']['database'],
)

universe_count = config['artnet']['universe_count']

mqtt_client_id = "PiXelTubeMaster-"+wlan_mac_address

# Function to register a tube in the database
def register_tube(mac_address):
    cur = db.cursor()
    
    # Check if the tube already exists in the database
    cur.execute("SELECT * FROM tubes WHERE mac_address = %s", (mac_address,))
    existing_tube = cur.fetchone()

    if existing_tube:
        # Tube already exists, do nothing for now
        pass
    else:
        # Tube is new, insert into the database
        cur.execute("INSERT INTO tubes (mac_address, universe, dmx_address, lamp_power) VALUES (%s, %s, %s, %s)",
                    (mac_address, 0, 1, 0))  # Universe 0, DMX Address 1, Lamp Power Off (False)
    cur.close()

# Registration system route
@app.route('/register_tube', methods=['POST'])
def register_tube_route():
    mac_address = request.form.get('mac_address')
    register_tube(mac_address)
    return jsonify({'success': True, 'message': 'Tube registered successfully.'})


@app.route('/get_assigned_params/<tube_unique_id>', methods=['GET'])
def get_assigned_params(tube_unique_id):
    try:
        cur = db.cursor()
        cur.execute("SELECT universe, dmx_address FROM tubes WHERE mac_address = %s", (tube_unique_id,))
        result = cur.fetchone()
        cur.close()

        if result:
            universe, dmx_address = result
            return jsonify({'success': True, 'universe': universe, 'dmx_address': dmx_address})
        else:
            return jsonify({'success': False, 'message': 'Tube not found in the database'})
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {e}'})

def flask_api():
    app.run(host='0.0.0.0', port=5000)

def get_eth0_ip():
    try:
        # Get the IP address of the eth0 interface
        eth0_ip = str(os.system("ip -4 -o addr show eth0 | awk '{print $4}' | cut -d '/' -f 1 "))
        return eth0_ip
    except (KeyError, IndexError, OSError) as e:
        print(f"Error getting eth0 IP: {e}")
        exit
    
def on_connect(client, userdata, flags, reason_code, properties):
        if reason_code == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", str(reason_code))

def connect_mqtt():
    # Set Connecting Client ID
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    # client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect("localhost", 1883)
    return client

def start_mqtt_publishers(universe_count):
    used_universes = universe_count
    print("universe count: "+str(used_universes))
    universe_list = list(range(0, used_universes))
    # Create and start a thread for each universe
    print(str(universe_list))
    mqtt_client = connect_mqtt()
    artnetBindIp = get_eth0_ip()
    artNet = Artnet.Artnet(BINDIP = artnetBindIp, DEBUG = True, SHORTNAME = "PiXelTubeMaster", LONGNAME = "PiXelTubeMaster", PORT = 6454, REFRESH=30)
    tuple_ip = (str(get_eth0_ip()), 6454)
    artNet.art_pol_reply(tuple_ip)
    try:
        while True:
            try:
                # Gets whatever the last Art-Net packet we received is
                artNetPacket = artNet.readPacket()
                # Make sure we actually *have* a packet
                if artNetPacket is not None and artNetPacket.data is not None:
                    #Checks to see if the current packet is for the specified DMX Universe
                    if artNetPacket.universe in universe_list:
                        dmxPacket = artNetPacket.data
                        # channel = 1
                        # for value in artNetPacket.data:
                        #     # Create MQTT topic based on the universe and channel
                        #     topic = f"{str(artNetPacket.universe)}/{str(channel)}"
                            
                        #     # Publish the DMX value to the MQTT topic
                        #     mqtt_client.publish(topic, str(value))
                        #     channel + 1
                        for i in range(512):
                            # Lists in python start at 0, 
                            print(dmxPacket[i-1], end=" ")
                            print(5)
                            
            except Exception as e:
                print(f"Error in universes {universe_list}: {e}")
            except KeyboardInterrupt:
                break
    except Exception as e:
        print(f"Error in universes {universe_list}: {e}")

if __name__ == "__main__":
    start_mqtt_publishers(universe_count)
    # flask_thread = threading.Thread(target=flask_api())
    # flask_thread.start()
    # flask_thread.join()
    
