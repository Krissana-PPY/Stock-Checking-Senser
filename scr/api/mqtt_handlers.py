from flask_socketio import SocketIO
from flask_mqtt import Mqtt
import api_utils
import globals_vars
import helpers

socketio = None
mqtt = None

def setup_mqtt(app):
    global socketio, mqtt
    socketio = SocketIO(app)
    app.config['MQTT_BROKER_URL'] = globals_vars.mqtt_broker_url
    app.config['MQTT_BROKER_PORT'] = globals_vars.mqtt_broker_port
    app.config['MQTT_USERNAME'] = globals_vars.mqtt_username
    app.config['MQTT_PASSWORD'] = globals_vars.mqtt_password
    app.config['MQTT_KEEPALIVE'] = globals_vars.mqtt_keepalive
    app.config['MQTT_TLS_ENABLED'] = globals_vars.mqtt_tls_enabled
    topic = "+"
    mqtt = Mqtt(app, connect_async=True)

    @mqtt.on_connect()
    def HandleConnect(client, userdata, flags, rc):
        """Handle MQTT connection event."""
        print("connect with result code " + str(rc))
        client.subscribe(topic)

    @mqtt.on_message()
    def HandleMqttMessage(client, userdata, message):
        """Handle incoming MQTT messages."""
        msg = message.payload.decode()
        print(message.topic + " " + str(msg))

        if globals_vars.current_id > 0:
            if globals_vars.last_row_id is None or globals_vars.current_id != getattr(HandleMqttMessage, 'last_id', None):
                row_id, page = api_utils.GetFirstRowId(globals_vars.current_id)
                HandleMqttMessage.last_id = globals_vars.current_id
                globals_vars.last_row_id = row_id
            else:
                row_id = globals_vars.last_row_id

        if message.topic == "measure":
            helpers.CollectSensorData(msg)

        elif message.topic == "finish":
            for i in range(len(globals_vars.distance)):
                helpers.CalDistacetrue(globals_vars.distance[i], globals_vars.angle_y[i])
            average_distance = helpers.CalculateAverageDistance()
            api_utils.PostEachPallet(row_id, globals_vars.sub_row, average_distance, 1, 1)

            if average_distance > 0:
                helpers.CalResultPallet(average_distance)
            else:
                globals_vars.sub_pallet.append(0)

            for i in range(1, len(globals_vars.sub_pallet) + 1):
                event_name = f'send_point_{i}'
                data = helpers.FormatPointData(globals_vars.sub_pallet[i - 1])
                socketio.emit(event_name, data, namespace='/')

            api_utils.PostRowPallet(row_id, globals_vars.sub_row, globals_vars.sub_pallet[-1])
            helpers.ClearLists(globals_vars.distance, globals_vars.angle_x, globals_vars.angle_y, globals_vars.distance_true)
            globals_vars.sub_row += 1

        elif message.topic == "NoProducts":
            print("No products detected")
            globals_vars.sub_pallet.append(0)
            api_utils.PostRowPallet(row_id, globals_vars.sub_row, globals_vars.sub_pallet[-1])
            helpers.ClearLists(globals_vars.distance, globals_vars.angle_x, globals_vars.angle_y, globals_vars.distance_true)
            globals_vars.sub_row += 1

        elif message.topic == "F":
            row_id, page = api_utils.GetFirstRowId(globals_vars.current_id)
            if row_id:
                socketio.emit('send_c_row', {'c_row_v': row_id})

        elif message.topic == "QR":
            if globals_vars.current_id == 0:
                globals_vars.current_id += 1
                print("START")
            elif globals_vars.current_id > 0:
                row_id, page = helpers.HandleNextRowOrQR(row_id)
                socketio.emit('send_c_row', {'c_row_v': row_id})

        elif message.topic == "B":
            helpers.ClearLists(
                globals_vars.distance,
                globals_vars.angle_x,
                globals_vars.angle_y,
                globals_vars.distance_true,
                globals_vars.sub_pallet
            )
            globals_vars.sub_row = 1
            globals_vars.current_id -= 1
            if globals_vars.current_id <= 1:
                globals_vars.current_id = 1
            row_id, page = api_utils.GetFirstRowId(globals_vars.current_id)
            if row_id:
                socketio.emit('send_c_row', {'c_row_v': row_id})
            socketio.emit('set_zero', helpers.FormatAllZero(), namespace='/')

        elif message.topic == "T":
            row_id, page = api_utils.GetFirstRowId(1)
            socketio.emit('send_c_row', {'c_row_v': row_id})
            print(f"Resetting to first row: {row_id}")

        elif message.topic == "READY":
            if current_id > 1:
                api_utils.DeleteDataInStock()
                current_id = 0
            elif current_id == 0:
                client.publish("OK", payload="I am ready") 

        elif message.topic == "CLEAR":
            api_utils.DeleteDataInStock()
            current_id = 0