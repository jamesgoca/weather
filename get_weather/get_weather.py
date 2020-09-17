import json
import datetime
from sense_hat import SenseHat

sense = SenseHat()
sense.clear()

get_temp = sense.get_temperature()
today = datetime.datetime.now()


with open ("data/temperature_data.json", "r") as file:
	data = json.load(file)

data.append(
	{
		"temp": get_temp,
		"time": today.strftime("%Y-%m-%d %H:%M:%S")
	}
)

with open("data/temperature_data.json", "w") as new_file:
	json.dump(data, new_file)
