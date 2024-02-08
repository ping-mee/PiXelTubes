import socket
from flask import Flask, render_template, request, jsonify
import json
import mysql.connector

app = Flask(__name__)

# Read configuration from config.json
try:
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)
except FileNotFoundError:
    # Create config.json with default values if it doesn't exist
    config = {
        "mysql": {
            "host": "localhost",
            "user": "root",
            "password": "",
            "database": "pixeltube_db"
        }
    }
    with open('config.json', 'w') as config_file:
        json.dump(config, config_file, indent=4)

database = config['mysql']['database']

db = mysql.connector.connect(
    host=config['mysql']['host'],
    user=config['mysql']['user'],
    password=config['mysql']['password'],
    database=config['mysql']['database'],
)

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
        mysql.connection.commit()

    cur.close()

# Registration system route
@app.route('/register_tube', methods=['POST'])
def register_tube_route():
    mac_address = request.form.get('mac_address')
    register_tube(mac_address)
    return jsonify({'success': True, 'message': 'Tube registered successfully.'})

# Function to retrieve registered tubes from the database
def get_tubes():
    cur = db.cursor()
    cur.execute("SELECT * FROM tubes")
    tubes = cur.fetchall()
    cur.close()
    return tubes

@app.route('/get_assigned_params/<tube_id>', methods=['GET'])
def get_assigned_params(tube_id):
    try:
        cur = db.cursor()
        cur.execute("SELECT universe, dmx_address FROM tubes WHERE mac_address = %s", (tube_id,))
        result = cur.fetchone()
        cur.close()

        if result:
            universe, dmx_address = result
            return jsonify({'success': True, 'universe': universe, 'dmx_address': dmx_address})
        else:
            return jsonify({'success': False, 'message': 'Tube not found in the database'})
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {e}'})

# Index route for the web interface
@app.route('/')
def index():
    tubes = get_tubes()
    return render_template('index.html', tubes=tubes)

def main():
    app.run(host='0.0.0.0', port=5000)

if __name__ == "__main__":
    main()
