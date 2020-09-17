import os
import json
import pyowm
import psutil
import datetime
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, send_from_directory

load_dotenv()

app = Flask(__name__)
owm = pyowm.OWM(os.environ.get("pyowm-key"))
mgr = owm.weather_manager()
observation = mgr.weather_at_place("{},GB".format(os.environ.get("location")))

@app.context_processor
def inject_color():
	forecast = observation.weather

	return dict(color_temp=forecast.temperature("celsius")["temp"])

@app.route("/")
def index():
	with open("get_weather/data/data.json") as file:
		data = json.load(file)

	forecast = observation.weather

	now = datetime.datetime.now()

	last_rpi_temp_check = datetime.datetime.strptime(data[-1]["time"], "%Y-%m-%d %H:%M:%S")

	last_updated_indoors = last_rpi_temp_check.strftime("%A %d %B at %H:%M:%S")

	return render_template("index.html",
		indoor_temp=round(int(data[-1]["temp"]), 2),
		indoor_pressure=round(int(data[-1]["pressure"]), 2),
		indoor_humidity=round(int(data[-1]["humidity"]), 2),
		outdoor_temp=forecast.temperature("celsius"),
		wind_speed=forecast.wind()["speed"],
		outdoor_humidity=forecast.humidity,
		time=now.strftime("%A %d %B at %H:%M:%S"),
		last_updated_indoors=last_updated_indoors
	)

@app.route("/stats")
def stats():
	cpu = str(psutil.cpu_percent())
	virtual_memory = psutil.virtual_memory()
	disk_usage = psutil.disk_usage()
	core_temp = psutil.sensors_temperatures()

	stats_to_send = {
		"cpu": cpu + "%",
		"memory_available": virtual_memory["available"],
		"memory_used": virtual_memory["used"],
		"memory_free": virtual_memory["free"],
		"disk_usage": disk_usage["percent"] + "%",
		"core_temp": core_temp["core_temp"][0]["current"]
	}

	return jsonify(stats_to_send)

@app.route("/data.json")
def get_data():
	return send_from_directory("get_weather/data/", "data.json")

@app.errorhandler(404) 
def not_found(error):
	return render_template("404.html"), 404

if __name__ == "__main__":
	app.run(host="0.0.0.0", debug=True)
