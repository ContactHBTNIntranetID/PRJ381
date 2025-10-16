import serial
import time
import sys

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

# ====== Serial Setup ======
SERIAL_PORT = 'COM9'  # Replace with your ESP32 port
BAUD_RATE = 115200

try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
except serial.SerialException as e:
    print(f"Error opening serial port {SERIAL_PORT}: {e}")
    sys.exit(1)

print(f"Listening to ESP32 on {SERIAL_PORT}...\n")

# ====== Initialize variables ======
temperature = None
humidity = None
lux = None
full = None
ir = None
visible = None
lightStatus = None
rainValue = None
rainStatus = None
latitude = None
longitude = None
dateTime = None

def parse_arduino_line(line):
    """
    Parses a single line from ESP32. Handles simple CSV format:
    temp,hum,lux,full,ir,vis,lightStatus,rain,rainStatus,lat,lon,dateTime
    (No emojis, easier to parse)
    """
    global temperature, humidity, lux, full, ir, visible
    global lightStatus, rainValue, rainStatus, latitude, longitude, dateTime
    
    try:
        parts = line.strip().split(',')
        if len(parts) != 12:
            return False
        
        # Assign to variables
        temperature = float(parts[0])
        humidity = float(parts[1])
        lux = float(parts[2])
        full = int(parts[3])
        ir = int(parts[4])
        visible = int(parts[5])
        lightStatus = parts[6]
        rainValue = int(parts[7])
        rainStatus = parts[8]
        latitude = float(parts[9])
        longitude = float(parts[10])
        dateTime = parts[11]
        
        return True
    except Exception as e:
        print("Parse error:", e)
        return False

while True:
    try:
        # Read line from ESP32
        line = ser.readline().decode('utf-8', errors='ignore').strip()
        if not line:
            continue

        # Parse the line
        if parse_arduino_line(line):
            # Print nicely formatted output
            print("========== SENSOR READINGS ==========")
            print(f"Temp       : {temperature} °C")
            print(f"Humidity   : {humidity} %")
            print(f"Lux        : {lux} (full={full}, ir={ir}, vis={visible}) - {lightStatus}")
            print(f"Rain       : {rainStatus}")
            print(f"GPS        : {latitude}, {longitude} UTC {dateTime}")
            print("=====================================\n")
        else:
            print("Invalid or incomplete line:", line)

    except KeyboardInterrupt:
        print("\nExiting...")
        break
    except Exception as e:
        print("Serial read error:", e)
        continue

ser.close()
