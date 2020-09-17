import os
import json
import pyowm
import datetime
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, send_from_directory

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

	now = datetime.datetime.now()

	return render_template("index.html",
		indoor_temp=round(int(data[-1]["temp"]), 2),
		indoor_pressure=round(int(data[-1]["pressure"]), 2),
		indoor_humidity=round(int(data[-1]["humidity"]), 2),
		outdoor_temp=forecast.temperature("celsius"),
		wind_speed=forecast.wind()["speed"],
		outdoor_humidity=forecast.humidity,
		time=now.strftime("%Y-%m-%d at %H:%M:%S")
	)

@app.route("/data.json")
def get_data():
	return send_from_directory("get_weather/data/", "data.json")

if __name__ == "__main__":
	app.run(host="0.0.0.0", debug=True)