# Sensor and pallet state variables
distance = []          # List to store measured distances
distance_true = []     # List to store calculated straight-line distances
angle_x = []           # List to store angles along the X-axis
angle_y = []           # List to store angles along the Y-axis
sub_pallet = []        # List to store the number of pallets in each sub-row
sub_row = 1            # Current sub-row number in a pallet row
current_id = 0         # Identifier for the current pallet
last_row_id = None     # Last row id

# MQTT Configuration
mqtt_broker_url = '192.168.4.100'
mqtt_broker_port = 1883
mqtt_username = ''
mqtt_password= ''
mqtt_keepalive = 300
mqtt_tls_enabled = False

# API URL
url = ""

