from flask import Flask, request, jsonify
import json
from MySQLdb import connect
import paho.mqtt.client as mqtt
import python_artnet as Artnet
import os
from getmac import get_mac_address
import time
from multiprocessing import Process, Pipe, Queue
from queue import Empty
import json

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

db = connect(
    host=config['mysql']['host'],
    user=config['mysql']['user'],
    password=config['mysql']['password'],
    database=config['mysql']['database'],
)

db.autocommit(True)

mqtt_client_id = "PiXelTubeMaster-"+wlan_mac_address

# Function to register a tube in the database
def register_tube(mac_address):
    cur1 = db.cursor()
    # Check if the tube already exists in the database
    cur1.execute("SELECT * FROM tubes WHERE mac_address = %s", (mac_address,))
    existing_tube = cur1.fetchone()

    # Check if the tube exsist. If it doesn't create a new db row
    if not existing_tube:
        cur1.execute("INSERT INTO tubes (mac_address, universe, dmx_address) VALUES (%s, %s, %s)",
        (mac_address, 0, 1))
    else:
        pass
    cur1.close()

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

def mqtt_publisher(ti_queue):
    tube_index = None
    # Create and start a thread for each universe
    mqtt_client = connect_mqtt()
    artnetBindIp = get_eth0_ip()
    artNet = Artnet.Artnet(BINDIP = artnetBindIp, DEBUG = True, SHORTNAME = "PiXelTubeMaster", LONGNAME = "PiXelTubeMaster", PORT = 6454)
    while True:
        try:
            # try:
            start = time.time()
            tube_index = ti_queue.get(block=False)
            end = time.time()
            print("Receiving of tube index took: "+str(end-start))
            tube_index_old = tube_index
            # except:
            #     if tube_index_old is not None:
            #         tube_index = tube_index_old
            #     else:
            #         tube_index = None
            # Gets whatever the last Art-Net packet we received is
            artNetPacket = artNet.readPacket()
            # Make sure we actually *have* a packet
            if artNetPacket is not None:
                if tube_index is not None:
                    for index_row in tube_index:
                        if artNetPacket.universe == int(index_row[1]):
                            dmx_address = int(index_row[2])
                            #Define RGB values per pixel
                            p1_g, p1_b, p1_r, p2_g, p2_b, p2_r, p3_g, p3_b, p3_r, p4_g, p4_b, p4_r, p5_g, p5_b, p5_r, p6_g, p6_b, p6_r = artNetPacket.data[dmx_address], artNetPacket.data[dmx_address+1], artNetPacket.data[dmx_address+2], artNetPacket.data[dmx_address+3], artNetPacket.data[dmx_address+4], artNetPacket.data[dmx_address+5], artNetPacket.data[dmx_address+6], artNetPacket.data[dmx_address+7], artNetPacket.data[dmx_address+8], artNetPacket.data[dmx_address+9], artNetPacket.data[dmx_address+10], artNetPacket.data[dmx_address+11], artNetPacket.data[dmx_address+12], artNetPacket.data[dmx_address+13], artNetPacket.data[dmx_address+14], artNetPacket.data[dmx_address+15], artNetPacket.data[dmx_address+16], artNetPacket.data[dmx_address+17]

                            # Pixel topics
                            p1_topic = "tube-"+str(index_row[0])+"/pixel_colors"

                            # Publish pixel topic
                            colors = [[p1_r, p1_g, p1_b], [p2_r, p2_g, p2_b], [p3_r, p3_g, p3_b], [p4_r, p4_g, p4_b], [p5_r, p5_g, p5_b], [p6_r, p6_g, p6_b]]
                            result_str = [str(color) for color in colors]
                            result = str(result_str)
                            mqtt_client.publish(p1_topic, result)
        except KeyboardInterrupt:
            artNet.close()

def tube_index_updater(ti_queue):
    while True:
        try:
            cur = db.cursor()
            cur.execute("SELECT mac_address, universe, dmx_address FROM tubes")
            tube_index = cur.fetchall()
            cur.close()
            ti_queue.put(tube_index)
        except Exception as e:
            print(e)
        time.sleep(5)

if __name__ == "__main__":
    (ti_receiver,ti_sender) = Pipe(True)
    ti_queue = Queue()
    ti_updater_thread = Process(target=tube_index_updater, args=(ti_queue, ))
    ti_updater_thread.start()
    publisher_thread = Process(target=mqtt_publisher, args=(ti_queue, ))
    publisher_thread.start()
    flask_thread = Process(target=flask_api)
    flask_thread.start()