# **System Overview**

---

## **1. API**

The API is hosted and operated on a *Raspberry Pi 3*. The files are located in the `api` folder. When used together with scripts in the `scrip` folder, the API will automatically start whenever the device is powered on.  
A simple web interface for initial testing is available in the `www` folder.

![Raspberry Pi 3](../images/Pi3.jpg)  
*Figure: Raspberry Pi 3*

---

## **2. Controller**

The *ESP32* acts as the controller, sending and receiving data to various modules such as the *Laser Distance Sensor LDS-50m*, *MPU6050 Gyroscope and Accelerometer*, and *YS-DIV268N-5A Stepper Motor Driver* to control the *Usongshine Nema17 Stepper Motor*.  
Data collected from these modules is sent to the API via MQTT in JSON format. All controller operations are located in the `control_laser` folder.

---

## **3. Access Point**

Another *ESP32* is configured as an access point to distribute Wi-Fi signals to devices and modules in this project. It also acts as a station to connect to the organization's or warehouse Wi-Fi and creates a NAT (Network Address Translation).

![Network Diagram](../images/Network.jpg)  
*Figure: Network Architecture*