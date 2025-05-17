# swp
smart watering pot using raspberry pi 3 B+ with grovepi+ v3.0

This Python script reads temperature, humidity, and soil moisture values from sensors connected to a Raspberry Pi 3 B+ with a GrovePi+ v3 board.

## Requirements

- **Hardware:**
  - Raspberry Pi 3 Model B+
  - GrovePi+ v3 board
  - DHT11 Temperature & Humidity Sensor (connected to D4)
  - Grove Capacitive Moisture Sensor v1.2 (connected to A0)

- **Software:**
  - Python 3
  - [grovepi Python library](https://github.com/DexterInd/GrovePi)

## Installation

1. **Install the GrovePi library:**
    ```sh
    git clone https://github.com/DexterInd/GrovePi.git
    cd GrovePi/Software/Python
    sudo python3 setup.py install
    ```

2. **Connect the sensors:**
    - DHT11 to digital port D4
    - Capacitive Moisture Sensor to analog port A0

3. **Clone or copy this repository to your Raspberry Pi.**

## Usage

Run the script with:

```sh
python3 main.py
```

You will see output similar to:

```
Temperature: 23 °C, Humidity: 45 %, Soil Moisture: 67.89 %
```

---
**Author:**  
[Samuel Schwarz]
