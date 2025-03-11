import pandas as pd
import time
import json
import paho.mqtt.client as mqtt

# Load the Excel file
file_path = r"\punch_data_updated.xlsx"
df = pd.read_excel(file_path)

# AWS IoT Core MQTT Configurations
AWS_ENDPOINT = "a2c52zdkyunxoy-ats.iot.ap-south-1.amazonaws.com"
TOPIC = "$aws/things/Strike-sense/shadow/update"  # Corrected Shadow Update Topic

CERT_PATH = r"\certs\70f532b4af9479f74a29297c222cfb1100a7f87351385b32c58ea59e32f25cfc-certificate.pem.crt"
KEY_PATH = r"\certs\70f532b4af9479f74a29297c222cfb1100a7f87351385b32c58ea59e32f25cfc-private.pem.key"
ROOT_CA_PATH = r"\certs\AmazonRootCA1.pem"

# MQTT Connection Callback


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to AWS IoT Core successfully!")
    else:
        print(f"Connection failed with return code {rc}")


# Initialize MQTT Client
client = mqtt.Client()
client.on_connect = on_connect
client.tls_set(ROOT_CA_PATH, certfile=CERT_PATH, keyfile=KEY_PATH)
client.connect(AWS_ENDPOINT, 8883, 60)

# Start MQTT Loop
client.loop_start()

# Send Data to AWS IoT Core in Shadow Format
for index, row in df.iterrows():
    # Convert row to dictionary
    punch_data = {
        "Punch Id": int(row["Punch Id"]),
        "Punch power (N)": float(row["Punch power (N)"]),
        "Punch Speed (km/h)": float(row["Punch Speed (km/h)"]),
        "Reflex time (ms)": float(row["Reflex time (ms)"]),
        "isblocked": int(row["isblocked"]),
        "timestamp": str(row["timestamp"])
    }

    # AWS IoT Shadow update format
    payload = json.dumps({

        "data": punch_data  # AWS IoT Shadow expects "state.reported"

    })

    # Publish message
    result = client.publish(TOPIC, payload, qos=1)

    if result.rc == 0:
        print(f"Sent data: {payload}")
    else:
        print(f"Failed to send data: {payload}")

    time.sleep(10)  # 1-second delay between messages

# Stop MQTT Loop and Disconnect
client.loop_stop()
client.disconnect()
print("Finished sending all data and disconnected from AWS IoT.")
