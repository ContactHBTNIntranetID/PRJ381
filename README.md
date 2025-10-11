# PRJ381
This project focuses on building an IoT-based system for real-time monitoring and automation. Using sensors, microcontrollers, and cloud services, it allows remote data access and control, improving efficiency, reducing manual tasks, and enabling smart decision-making.

## Arduino API set up

## 🛠️ Hardware Requirements

| Component              | Quantity | Notes                                |
|------------------------|----------|--------------------------------------|
| ESP32 Development Board| 1        | Any ESP32 board with WiFi            |
| DHT11 Sensor           | 1        | Temperature & Humidity               |
| TSL2591 Light Sensor   | 1        | I2C digital light sensor             |
| Rain Sensor Module     | 1        | Digital output (DO pin)              |
| NEO-6M GPS Module      | 1        | UART communication                   |
| Jumper Wires           | ~15      | Male-to-female recommended           |
| Breadboard             | 1        | Optional but helpful                 |
| USB Cable              | 1        | For power and programming            |

## 🔌 Wiring Connections
### DHT11 Temperature & Humidity Sensor
    DHT11 VCC    →  ESP32 3.3V
    DHT11 GND    →  ESP32 GND
    DHT11 DATA   →  ESP32 GPIO 23
### TSL2591 Light Sensor (I2C)
    TSL2591 VIN  →  ESP32 3.3V  ⚠️ (NOT 5V!)
    TSL2591 GND  →  ESP32 GND
    TSL2591 SDA  →  ESP32 GPIO 21
    TSL2591 SCL  →  ESP32 GPIO 22
### Rain Sensor Module
    Rain VCC     →  ESP32 3.3V  ⚠️ (Recommended for 3.3V logic)
    Rain GND     →  ESP32 GND
    Rain DO      →  ESP32 GPIO 19
### NEO-6M GPS Module
    GPS VCC      →  ESP32 3.3V or 5V
    GPS GND      →  ESP32 GND
    GPS TX       →  ESP32 GPIO 16 (RX2)
    GPS RX       →  ESP32 GPIO 17 (TX2)
    
## 💻 In Arduino IDE:
  - You are going to hav to look for the sketch where the code is (Synched code)
  - Look for the code where you connect the code to a wifi signal

        const char* ssid = "YOUR_WIFI_SSID";         // Your WiFi network name
        const char* password = "YOUR_WIFI_PASSWORD"; // Your WiFi password

