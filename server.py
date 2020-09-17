import json
import pyowm
import os
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template

load_dotenv()

app = Flask(__name__)
owm = pyowm.OWM(os.environ.get("pyowm-key"))
mgr = owm.weather_manager()
observation = mgr.weather_at_place('London,GB')

COUNTRY = "UK"

@app.route("/")
def index():
	with open("get_weather/data/data.json") as file:
		data = json.load(file)

	forecast = observation.weather

	return render_template("index.html",
		indoor_temp=data[-1]["temp"],
		indoor_pressure=data[-1]["pressure"],
		indoor_humidity=data[-1]["humidity"],
		outdoor_temp=forecast.humidity,
		wind_speed=forecast.wind()["speed"],
		outdoor_humidity=forecast.temperature("celsius"),
	)

if __name__ == "__main__":
	app.run(host="0.0.0.0", debug=True)