import socket
from flask import Flask, render_template, request, jsonify
from flask_mysqldb import MySQL
from pythonosc import udp_client, dispatcher, osc_server

app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'  # Change to your MySQL host
app.config['MYSQL_USER'] = 'your_username'  # Change to your MySQL username
app.config['MYSQL_PASSWORD'] = 'your_password'  # Change to your MySQL password
app.config['MYSQL_DB'] = 'your_database'  # Change to your MySQL database name

mysql = MySQL(app)

# Art-Net settings
ARTNET_PORT_IN = 6454  # Standard Art-Net input port
ARTNET_PORT_OUT = 6455  # Standard Art-Net output port

# IP addresses of the source and destination networks
SOURCE_NETWORK_IP = '10.0.0.1'
DESTINATION_NETWORK_IP = '192.168.0.1'

# Create an Art-Net dispatcher
artnet_dispatcher = dispatcher.Dispatcher()

def forward_artnet_handler(address, *args):
    # Create an Art-Net packet from the received OSC message
    artnet_packet = b'Art-Net\x00' + b'\x00' * 7 + bytes(args[0], 'utf-8') + b'\x00' * 2 + b'\x00\x00'
    
    # Send the Art-Net packet to the destination network
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.sendto(artnet_packet, (DESTINATION_NETWORK_IP, ARTNET_PORT_OUT))

# Map the Art-Net handler to the OSC address
artnet_dispatcher.map('/artnet', forward_artnet_handler)

# Create an Art-Net server listening on the source network
artnet_server = osc_server.ThreadingOSCUDPServer((SOURCE_NETWORK_IP, ARTNET_PORT_IN), artnet_dispatcher)
artnet_server_thread = artnet_server.serve_forever()

# Function to register a tube in the database
def register_tube(mac_address):
    cur = mysql.connection.cursor()
    
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
        mysql.connection.commit()

    cur.close()

# Registration system route
@app.route('/register_tube', methods=['POST'])
def register_tube_route():
    mac_address = request.form.get('mac_address')
    register_tube(mac_address)
    return jsonify({'success': True, 'message': 'Tube registered successfully.'})

# Your other routes and functions for toggling and retrieving tube information

# ... (your registration system code)

# Function to retrieve registered tubes from the database
def get_tubes():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM tubes")
    tubes = cur.fetchall()
    cur.close()
    return tubes

# Index route for the web interface
@app.route('/')
def index():
    tubes = get_tubes()
    return render_template('index.html', tubes=tubes)

# ... (your registration system code)

def main():
    app.run(host='127.0.0.1', port=5000)

if __name__ == "__main__":
    main()
