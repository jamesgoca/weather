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

temp = sense.get_temperature()

# Add data to JSON data file

data.append(
	{
		"temp": temp,
		"pressure": sense.get_pressure(),
		"humidity": sense.get_humidity(),
		"time": today.strftime("%Y-%m-%d %H:%M:%S")
	}
)

# Write new data to file

with open("/home/james/weather/get_weather/data/data.json", "w") as new_file:
	json.dump(data, new_file)

orange = [255,69,0]
yellow = [255,255,0]
blue = 	[0,0,255]
dark_blue = [0,0,139]

print(dark_blue * 64)

if temp <= 2:
	color_array = dark_blue * 64
elif temp >= 3 and temp <= 8:
	color_array = blue * 64
elif temp >= 9 and temp <= 15:
	color_array = yellow * 64
else:
	color_array = orange * 64

sense.set_pixels(color_array)
