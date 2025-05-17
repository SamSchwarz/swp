from flask import Flask, jsonify, send_from_directory
import sqlite3
import os

app = Flask(__name__)

DB_PATH = os.path.join(os.path.dirname(__file__), "sensor_data.db")

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/data')
def data():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT timestamp, temperature, humidity, soil_moisture FROM readings ORDER BY timestamp DESC")
    rows = c.fetchall()
    conn.close()
    # Convert to list of dicts
    data = [
        {
            "timestamp": row[0],
            "temperature": row[1],
            "humidity": row[2],
            "soil_moisture": row[3]
        }
        for row in rows
    ]
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)