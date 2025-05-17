import grovepi
import sys
import os
import sqlite3  # <-- Add this import
from datetime import datetime  # For timestamp

# DHT11 connected to D4 port
sensor = 4             # D4 port
soil_sensor = 0       # A0 port

max_moisture = 191 # value which the sensor returns when fully submerged in water
min_moisture = 470 # value which the sensor returns when fully dry
moisture = 0

# Function to suppress unwanted prints from grovepi.dht
def suppress_prints():
    original_stdout = sys.stdout
    sys.stdout = open(os.devnull, 'w')
    return original_stdout

# Function to calculate moisture percentage
def get_moisture_percentage(value):
    # Clamp value between max_moisture (wet) and min_moisture (dry)
    if value < max_moisture:
        value = max_moisture
    elif value > min_moisture:
        value = min_moisture
    # Calculate percentage: 0% (dry) to 100% (wet)
    percentage = 100 * (min_moisture - value) / (min_moisture - max_moisture)
    return max(0.0, min(percentage, 100.0))

# Initialize the database and table
def init_db():
    conn = sqlite3.connect("sensor_data.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS readings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            temperature REAL,
            humidity REAL,
            soil_moisture REAL
        )
    ''')
    conn.commit()
    conn.close()

# Store a reading in the database
def store_reading(temp, hum, soil_moisture):
    conn = sqlite3.connect("sensor_data.db")
    c = conn.cursor()
    c.execute('''
        INSERT INTO readings (timestamp, temperature, humidity, soil_moisture)
        VALUES (?, ?, ?, ?)
    ''', (datetime.now().isoformat(), temp, hum, soil_moisture))
    conn.commit()
    conn.close()

def main():
    init_db()  # Initialize DB on start
    try:
        # Suppress unwanted prints from grovepi.dht
        original_stdout = suppress_prints()
        # Read temperature and humidity from DHT11
        temp, hum = grovepi.dht(sensor, 0)  # 0 for DHT11
        # Restore original stdout
        sys.stdout = original_stdout
        # Read soil moisture from the sensor

        moisture = grovepi.analogRead(soil_sensor)
        # Calculate moisture percentage
        soil_moisture = get_moisture_percentage(moisture)

        # Print the results
        if temp is not None and hum is not None:
            print("Temperature: {} °C, Humidity: {} %, Soil Moisture: {:.2f} %".format(temp, hum, soil_moisture))
            store_reading(temp, hum, soil_moisture)  # Store in DB
        else:
            print("Sensor read failed.")
    except IOError:
        print("IOError - check connection or sensor type.")

if __name__ == "__main__":
    main()