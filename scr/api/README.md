# IOT-SensorTB API

This API connects and manages data from IoT SensorTB devices using Flask, MQTT, and SocketIO. It receives sensor data, processes it, and controls operations via a web interface.

## Project Structure

```
scr/
  api/
    ├── flask_api.py         # Flask web server and main API
    ├── mqtt_handlers.py     # Handles MQTT and SocketIO
    ├── helpers.py           # Functions for processing sensor data
    ├── api_utils.py         # Functions for connecting to external REST APIs
    ├── globals_vars.py      # Global variables for state and config
    ├── README.md            # Documentation
```

## Installation

### 1. Install Python and dependencies

```bash
sudo apt update
sudo apt install -y python3 python3-pip
pip3 install flask flask-socketio flask-mqtt mysql-connector-python eventlet gevent
```

### 2. Install and setup MySQL

```bash
sudo apt install -y mysql-server
sudo systemctl start mysql
sudo systemctl enable mysql
```
- Create database and import tables:
```sql
CREATE DATABASE your_database_name;
USE your_database_name;
-- Import your DATA.sql here
SHOW TABLES;
```

### 3. Install and configure Mosquitto MQTT Broker

```bash
sudo apt install -y mosquitto mosquitto-clients
sudo systemctl enable mosquitto
sudo systemctl start mosquitto
sudo systemctl status mosquitto
sudo nano /etc/mosquitto/conf.d/myconf.conf
```

    listener 1883
    allow_anonymous true

```bash
sudo systemctl stop mosquitto
sudo mosquitto -v -c /etc/mosquitto/conf.d/myconf.conf
sudo systemctl daemon-reload
sudo systemctl restart mosquitto
sudo systemctl status mosquitto
sudo systemctl enable mosquitto
```

### 4. install services

```bash
chmod +x /home/<name>/IOT-SenserTB/scrip/start_services.sh
sudo systemctl daemon-reload
sudo systemctl enable iot_senser_tb.service
sudo systemctl start iot_senser_tb.service
```

### 3. Install and configure Mosquitto MQTT Broker

```bash
sudo apt install chromium-browser
```

## Usage

1. Configure MQTT and API URLs in `globals_vars.py`.
2. Start the Flask API:

   ```bash
   python3 flask_api.py
   ```
3. Access the web interface at `http://localhost:5000`.

## MQTT Topics

- `measure` : Receive sensor data
- `finish` : Process data and calculate pallet count
- `NoProducts` : When no products are detected
- `QR`, `B`, `T`, `READY`, `CLEAR` : Control workflow

## API Endpoints

- `GET /` : Main web page
- `POST /send_command` : Send MQTT commands from the web

## External REST API

- Functions in `api_utils.py` connect to external APIs to fetch row, area, and save pallet data.

## Testing

- Use Postman or curl to test API and MQTT.
- Check results via the web interface and console logs.

## Configuration

- Adjust settings in `globals_vars.py` as needed.
- To add new features, extend functions in `helpers.py` or `mqtt_handlers.py`.