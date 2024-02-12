from flask import Flask, render_template, request, jsonify
import json
import MySQLdb
import paho.mqtt.client as mqtt
import threading
from stupidArtnet import StupidArtnet
import os
from getmac import get_mac_address
import netifaces

app = Flask(__name__)

wlan_mac_address = get_mac_address(interface="wlan0")

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
        eth0_ip = netifaces.ifaddresses('eth0')[netifaces.AF_INET][0]['addr']
        return eth0_ip
    except (KeyError, IndexError, OSError) as e:
        print(f"Error getting eth0 IP: {e}")
        return None


def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect to MQTT broker, return code %d\n", rc)

    client = mqtt.Client(mqtt_client_id)
    client.on_connect = on_connect()
    client.connect("localhost", 1883)
    return client


def mqtt_publisher(universe):
    mqtt_client = connect_mqtt()
    try:
        # Create a new Art-Net listener
        artnet = StupidArtnet(bind=get_eth0_ip())
        artnet.start(universe=universe)

        while True:
            dmx_values = artnet.listen()

            if dmx_values is not None:
                for channel, value in enumerate(dmx_values):
                    # Create MQTT topic based on the universe and channel
                    topic = f"/{universe}/{channel}"
                    
                    # Publish the DMX value to the MQTT topic
                    mqtt_client.publish(topic, payload=value, qos=0, retain=False)
                    print(str(universe+" "+channel+" "+value))

    except Exception as e:
        print(f"Error in universe {universe}: {e}")

def start_mqtt_publishers(universe_count):
    used_universes = universe_count - 1
    universes_to_publish = list(range(1, used_universes + 1))
    # Create and start a thread for each universe
    threads = [threading.Thread(target=mqtt_publisher, args=(universe,)) for universe in universes_to_publish]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    start_mqtt_publishers(universe_count)
    flask_thread = threading.Thread(target=flask_api())
    flask_thread.start()
    flask_thread.join()
    
