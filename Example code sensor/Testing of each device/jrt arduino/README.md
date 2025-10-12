# **Laser Distance Sensor LDS-50m**

**Model:** *LDS-50m (b240422g-1)*

---

The LDS-50m is a compact laser distance sensor module capable of measuring distances up to 50 meters. It operates by emitting a laser beam that reflects off a target object, then calculates the distance based on the time-of-flight or phase shift of the reflected light. This sensor offers high accuracy, with measurements precise to the millimeter level.

Non-contact measurement allows for distance detection without physical contact with the target object. Its small size makes it suitable for integration into various devices and systems. The sensor supports easy connectivity, typically via serial (UART) communication, making it compatible with microcontrollers such as Arduino or ESP32.

---

## **Product Image**

![LDS-50m Sensor](/images/LDS-50m.jpg)  

---

## **Specifications**

- **Product Name:** Laser Distance Sensor  
- **Model Number:** *LDS-50m (b240422g-1)*  
- **Certification:** FDA / ISO9001 / CE / FCC / ROHS  
- **Accuracy:** ±1 mm (0.04 inch)  
- **Measuring Unit:** meter / inch / feet  
- **Measuring Range (without Reflection):** 0.03–40 m  
- **Measuring Time:** 0.125–4 seconds  
- **Laser Class:** Class II  
- **Laser Type:** 635 nm, <1 mW  
- **Size:** 45 × 25 × 12 mm (±1 mm)  
- **Weight:** About 10 g  
- **Voltage:** DC 2.0–3.3 V  
- **Electrical Level:** TTL / CMOS  
- **Frequency:** 3 Hz–8 Hz  
- **Operating Temperature:** 0–40 °C (32–104 °F)  
- **Storage Temperature:** –25–60 °C (–13–140 °F)  
- **Packaging:** Neutral packing

---

## **Serial Commands**

The LDS-50m sensor can be controlled via serial commands. Below is a summary of available commands:

| No. | Command | Function | ASCII Code | HEX Code |
|-----|---------|----------|------------|----------|
| 1   | **O**   | Turn on the laser. The module returns a confirmation string. | 0x4F | O |
| 2   | **C**   | Turn off the laser. The module returns a confirmation string. | 0x43 | C |
| 3   | **S**   | Read module status. Returns temperature and input voltage, e.g., `"18.0'C, 3.0V"` | 0x53 | S |
| 4   | **D**   | Start automatic measurement. Returns distance and signal quality, e.g., `"12.345m, 79"` | 0x44 | D |
| 5   | **M**   | Start slow measurement (highest accuracy). Returns as D command. | 0x4D | M |
| 6   | **F**   | Start fast measurement (lowest accuracy). Returns as D command. | 0x46 | F |
| 7   | **V**   | Query module version info. Returns serial and software version, e.g., `"170225002929456"` | 0x56 | V |
| 8   | **X**   | Power off the module and pull PWR_ON pin low. | 0x58 | X |

---

### **Notes**

- If the measured distance is less than 10 meters, the 10-meter position in the returned string is filled with a space character to keep the string length consistent.
- Lower signal quality values indicate better signal; higher values indicate worse reflected signal.
- Automatic measurement adjusts speed for accuracy depending on the reflector condition.
- If ranging fails, the command returns an error string `"Er.XX!"`, where `XX` is the error number (refer to the error list for details).
- The **M** command provides the slowest speed but highest accuracy.
- The **F** command provides the fastest speed but lowest accuracy; use in good reflection conditions.