from flask import Flask, render_template, request, jsonify, send_from_directory
import logging
import mqtt_handlers

def CreateApp():
    """Create and configure the Flask application."""
    app = Flask(__name__, template_folder='www/')
    app.config['SECRET_KEY'] = 'secret_key'

    return app

app = CreateApp()
mqtt_handlers.setup_mqtt(app)  # config MQTT

# SocketIO Handlers to communicate with the client
@mqtt_handlers.socketio.on('connect')
def HandleConnect():
    """Handle client connection."""
    print('Client connected')
    mqtt_handlers.socketio.emit('message', 'Connected to server')

@mqtt_handlers.socketio.on('message')
def HandleMessage(message):
    """Handle incoming messages from the client."""
    print('Received message:', message)

# Routes to render HTML pages
@app.route("/")
def Index():
    """Render the main HTML page."""
    return render_template("index.html")

@app.route("/test_control_sensor.html")
def TestControlSensor():
    """Render the test control sensor HTML page."""
    return render_template("test_control_sensor.html")

@app.route('/index.html')
def index_html():
    return render_template("index.html")

@app.route('/service-worker.js')
def service_worker():
    return send_from_directory('static', 'service-worker.js')

@app.route('/send_command', methods=['POST'])
def SendCommand():
    """Handle sending commands via MQTT."""
    data = request.get_json()
    topic = data.get('topic')
    if topic:
        try:
            mqtt_handlers.mqtt.publish(topic, '')
            return jsonify({'status': 'success'}), 200
        except Exception as e:
            logging.error(f"Error publishing topic {topic}: {e}")
            return jsonify({'status': 'error', 'message': 'Failed to publish topic'}), 500
    return jsonify({'status': 'error', 'message': 'Invalid topic'}), 400

if __name__ == "__main__":
    mqtt_handlers.socketio.run(app, host='0.0.0.0', port=5000, allow_unsafe_werkzeug=True)