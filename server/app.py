from flask import Flask, render_template, request, jsonify
import json
import MySQLdb
import paho.mqtt.client as mqtt
import threading
import python_artnet as Artnet
import os
from getmac import get_mac_address
import time
import sys
from multiprocessing import Process

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

db.autocommit(True)
cur = db.cursor()

mqtt_client_id = "PiXelTubeMaster-"+wlan_mac_address

# Function to register a tube in the database
def register_tube(mac_address):
    
    # Check if the tube already exists in the database
    cur.execute("SELECT * FROM tubes WHERE mac_address = %s", (mac_address,))
    existing_tube = cur.fetchone()

    # Check if the tube exsist. If it doesn't create a new db row
    if not existing_tube:
        cur.execute("INSERT INTO tubes (mac_address, universe, dmx_address) VALUES (%s, %s, %s)",
        (mac_address, 0, 1))
    else:
        pass
    cur.close()

# Registration system route
@app.route('/register_tube', methods=['POST'])
def register_tube_route():
    mac_address = request.form.get('mac_address')
    register_tube(str(mac_address))
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
    app.run(host='192.168.0.1', port=5000)

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

def start_mqtt_publishers():
    # Create and start a thread for each universe
    mqtt_client = connect_mqtt()
    artnetBindIp = get_eth0_ip()
    artNet = Artnet.Artnet(BINDIP = artnetBindIp, DEBUG = True, SHORTNAME = "PiXelTubeMaster", LONGNAME = "PiXelTubeMaster", PORT = 6454)
    while True:
        try:
            # Gets whatever the last Art-Net packet we received is
            artNetPacket = artNet.readPacket()
            # Make sure we actually *have* a packet
            if artNetPacket is not None:
                #Checks to see if the current packet is for the specified DMX Universe
                dmxPacket = artNetPacket.data
                # Create MQTT topic based on the universe and channel
                cur.execute("SELECT mac_address, universe, dmx_address FROM tubes")
                result = cur.fetchall()
                for row in result:
                    dmx_address = int(row[2])
                    if artNetPacket.universe == int(row[2]):
                        #Define RGB values per pixel
                        p1_r = dmxPacket[dmx_address+0+0]
                        p1_g = dmxPacket[dmx_address+0+1]
                        p1_b = dmxPacket[dmx_address+0+2]

                        p2_r = dmxPacket[dmx_address+3+0]
                        p2_g = dmxPacket[dmx_address+3+1]
                        p2_b = dmxPacket[dmx_address+3+2]

                        p3_r = dmxPacket[dmx_address+6+0]
                        p3_g = dmxPacket[dmx_address+6+1]
                        p3_b = dmxPacket[dmx_address+6+2]

                        p4_r = dmxPacket[dmx_address+9+0]
                        p4_g = dmxPacket[dmx_address+9+1]
                        p4_b = dmxPacket[dmx_address+9+2]

                        p5_r = dmxPacket[dmx_address+12+0]
                        p5_g = dmxPacket[dmx_address+12+1]
                        p5_b = dmxPacket[dmx_address+12+2]

                        p6_r = dmxPacket[dmx_address+15+0]
                        p6_g = dmxPacket[dmx_address+15+1]
                        p6_b = dmxPacket[dmx_address+15+2]

                        # Pixel topics
                        p1_topic = "tube-"+str(result[1])+"/p1"
                        p2_topic = "tube-"+str(result[1])+"/p2"
                        p3_topic = "tube-"+str(result[1])+"/p3"
                        p4_topic = "tube-"+str(result[1])+"/p4"
                        p5_topic = "tube-"+str(result[1])+"/p5"
                        p6_topic = "tube-"+str(result[1])+"/p6"

                        # Publish pixel topic
                        mqtt_client.publish(p1_topic, str([p1_r, p1_g, p1_b]))
                        mqtt_client.publish(p2_topic, str([p2_r, p2_g, p2_b]))
                        mqtt_client.publish(p3_topic, str([p3_r, p3_g, p3_b]))
                        mqtt_client.publish(p4_topic, str([p4_r, p4_g, p4_b]))
                        mqtt_client.publish(p5_topic, str([p5_r, p5_g, p5_b]))
                        mqtt_client.publish(p6_topic, str([p6_r, p6_g, p6_b]))

        except KeyboardInterrupt:
            artNet.close()
            sys.exit()

if __name__ == "__main__":
    flask_thread = Process(target=flask_api)
    flask_thread.start()
    publisher_thread = Process(target=start_mqtt_publishers)
    publisher_thread.start()
