# **MQTT**

**MQTT (Message Queue Telemetry Transport)** is a protocol designed for data transmission in IoT systems. It operates on a **Broker and Clients Network** model and is engineered for real-time, low-volume data transfer, resulting in low power consumption. Unlike TCP/IP, which uses one-to-one communication and consumes more resources, MQTT is ideal for IoT systems where devices frequently send and receive data, and a single device may communicate with multiple devices or broadcast to all.

- **Broker (Server)**: Acts as an intermediary, receiving data from publishers and sending it to subscribers.
- **Publisher**: Sends data to a topic on the broker (*publishing*).
- **Subscriber**: Receives data from a topic on the broker (*subscribing*).
- **Topic**: The subject or channel for data exchange between publishers and subscribers.

---

## **Eclipse Mosquitto**

**Eclipse Mosquitto** is an open-source MQTT broker that implements the MQTT protocol. MQTT is a lightweight protocol designed for devices with limited resources and low bandwidth, making it suitable for **Machine-to-Machine (M2M)** or **Internet of Things (IoT)** applications.