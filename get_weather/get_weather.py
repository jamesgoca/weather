import json
import datetime
from sense_hat import SenseHat

# Initialize Sense HAT

sense = SenseHat()
sense.clear()

today = datetime.datetime.now()

# Read data

with open ("/home/james/weather/get_weather/data/data.json", "r") as file:
	data = json.load(file)

# Add data to JSON data file

data.append(
	{
		"temp": sense.get_temperature(),
		"pressure": sense.get_pressure(),
		"humidity": sense.get_humidity(),
		"time": today.strftime("%Y-%m-%d %H:%M:%S")
	}
)

# Write new data to file

with open("/home/james/weather/get_weather/data/data.json", "w") as new_file:
	json.dump(data, new_file)
