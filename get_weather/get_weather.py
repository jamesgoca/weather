import os
import json
import pyowm
import datetime
from sense_hat import SenseHat
from dotenv import load_dotenv

load_dotenv()

# Initialize OWM

owm = pyowm.OWM(os.environ.get("pyowm-key"))
mgr = owm.weather_manager()
observation = mgr.weather_at_place("{},GB".format(os.environ.get("location")))

forecast = observation.weather

outdoor_temp = forecast.temperature("celsius")["temp"]

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

orange = [255,69,0]
yellow = [255,255,0]
blue = 	[0,0,255]
dark_blue = [0,0,139]

if outdoor_temp <= 2:
	color_array = [dark_blue] * 64
elif outdoor_temp >= 3 and outdoor_temp <= 8:
	color_array = [blue] * 64
elif outdoor_temp >= 9 and outdoor_temp <= 15:
	color_array = [yellow] * 64
else:
	color_array = [orange] * 64

sense.set_pixels(color_array)
