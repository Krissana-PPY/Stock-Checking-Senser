# **Robot Laser Control System**

---

## **Overview**

The *Robot Laser Control System* is designed for automated measurement and control using a laser distance sensor, stepper motor, and motion tracking via an MPU6050 module. This system is suitable for applications requiring precise distance measurement and motorized movement, such as warehouse automation or robotic pallet handling.

---

## **Features**

- **Laser Distance Measurement:** Utilizes the LDS-50m sensor for accurate, non-contact distance readings up to 50 meters.
- **Stepper Motor Control:** Employs a Nema17 stepper motor for precise positioning.
- **Motion Tracking:** Integrates the MPU6050 gyroscope and accelerometer for orientation feedback.
- **Wireless Communication:** Supports WiFi and MQTT for remote monitoring and control.
- **Multi-Floor Operation:** Automated logic for handling multiple floors or levels.

---

## **System Architecture**

The system consists of the following main components:

- **Laser Distance Sensor (LDS-50m)**
- **Stepper Motor (Usongshine Nema17)**
- **Stepper Motor Driver (YS-DIV268N-5A)**
- **MPU6050 Motion Sensor**
- **ESP32 Microcontroller**

---

## **Images**

### **Laser Distance Sensor**

![LDS-50m Sensor](/images/LDS-50m.jpg)

### **Stepper Motor**

![Nema17 Stepper Motor](/images/Nema17.jpg)

### **Stepper Motor Driver**

![YS-DIV268N-5A Driver](/images/Drivemotor.jpg)

### **MPU6050 Sensor**

![MPU6050 Sensor](/images/MPU6050.jpg)

---

## **Getting Started**

1. **Hardware Setup**
   - Connect the LDS-50m sensor to the ESP32 via UART.
   - Wire the Nema17 stepper motor and YS-DIV268N-5A driver to the ESP32.
   - Connect the MPU6050 sensor via I2C.

2. **Software Setup**
   - Install required Arduino libraries: `PubSubClient`, `ArduinoJson`, `MPU6050_6Axis_MotionApps20`.
   - Configure WiFi and MQTT settings in `laser_parameter.h`.
   - Upload the firmware (`Robot_laser_control.ino`) to the ESP32.

---

## **Operation**

- The system connects to WiFi and MQTT broker for remote control.
- Receives commands via MQTT topics to initiate measurement or movement.
- Measures distance using the laser sensor and adjusts motor position accordingly.
- Publishes measurement data and status updates to MQTT topics.

---

## **MQTT Topics**

| **Topic**      | **Description**                  |
|----------------|----------------------------------|
| `F`            | Move forward                     |
| `B`            | Move backward                    |
| `done`         | Operation completed              |
| `2F`           | Two floors operation             |
| `3F`           | Three floors operation           |
| `test`         | Test operation                   |
| `error`        | Error reporting                  |
| `measure`      | Measurement data                 |
| `finish`       | Finish notification              |
| `NoProducts`   | No products detected             |

## **Parameter Explanations**

- `STEP_ANGLE 0.1125`:  
  The angle (in degrees) that the stepper motor rotates per step. For Nema17, this is typically 0.1125° per step.

- `float angle_rad = atan(0.80 / distanceOfmotor)`:  
  Calculates the angle in radians between a fixed distance of 0.80 meters and the current motor distance. Used for positioning calculations.

- `float angle_rad_lasor = atan(0.40 / distanceOfmotor)`:  
  Calculates the angle in radians between a fixed distance of 0.40 meters and the current motor distance. Used for laser alignment.

- `float degree = (atan(1.6 / 16)) * 180 / M_PI`:  
  Converts the arctangent of (1.6 / 16) from radians to degrees. Useful for determining the required rotation angle.

- `distanceOfmotor = distanceOfstart * cos(atan(1.6 / 16))`:  
  Calculates the effective motor travel distance based on the starting distance and the calculated angle.