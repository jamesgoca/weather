import os
import csv
import json
import pyowm
import psutil
import datetime
import time
import numpy as np
from sense_hat import SenseHat
from gpiozero import CPUTemperature
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, send_from_directory, request

load_dotenv()
sense = SenseHat()

app = Flask(__name__)
owm = pyowm.OWM(os.environ.get("pyowm-key"))
mgr = owm.weather_manager()
observation = mgr.weather_at_place("{},GB".format(os.environ.get("location")))

@app.context_processor
def inject_color():
	forecast = observation.weather

	now = datetime.datetime.now()

	time = now.strftime("%A %d %B at %H:%M:%S")

	return dict(
		color_temp=forecast.temperature("celsius")["temp"],
		time=time
	)

@app.route("/")
def index():
	with open("get_weather/data/data.json") as file:
		data = json.load(file)

	forecast = observation.weather

	last_rpi_temp_check = datetime.datetime.strptime(data[-1]["time"], "%Y-%m-%d %H:%M:%S")

	last_updated_indoors = last_rpi_temp_check.strftime("%A %d %B at %H:%M:%S")

	return render_template("index.html",
		indoor_temp=round(int(data[-1]["temp"]), 2),
		indoor_pressure=round(int(data[-1]["pressure"]), 2),
		indoor_humidity=round(int(data[-1]["humidity"]), 2),
		outdoor_temp=forecast.temperature("celsius"),
		wind_speed=forecast.wind()["speed"],
		outdoor_humidity=forecast.humidity,
		last_updated_indoors=last_updated_indoors
	)

@app.route("/stats")
def stats():
	cpu = psutil.cpu_percent()
	virtual_memory = psutil.virtual_memory()
	disk_usage = psutil.disk_usage("/")

	uptime = time.time() - psutil.boot_time()

	stats_to_send = {
		"cpu": str(cpu) + "%",
		"memory_available": str(virtual_memory[1]),
		"memory_used": str(virtual_memory[2]) + "%",
		"memory_free": str(virtual_memory[3]),
		"disk_usage": str(disk_usage[3]) + "%",
		"temperature": str(CPUTemperature().temperature) + " degrees celcius",
		"uptime": str(uptime) + " seconds"
	}

	return jsonify(stats_to_send)

@app.route("/webmentions", methods=["POST"])
def webmentions():
	if request.data["secret"] == os.environ.get("webmention-secret"):
		sense.clear()

		green = (0, 0, 255)

		pixel_array = [green * 64]

		sense.set_pixels(pixel_array)

		message = { "message": "Success." }

		return jsonify(message)
	else:
		message = { "message": "Not authenticated." }

		return jsonify(message), 403

@app.route("/colors", methods=["POST"])
def color_set():
	data = {
		"x": request.json.get("x"),
		"y": request.json.get("y"),
		"color": [255, 255, 254]
	}

	with open("grid.csv", "r") as file:
		grid_rows = []
		reader = csv.reader(file)

		for x in reader:
			grid_rows.append(x)

	new_array = np.array(grid_rows).astype(np.int)

	split_array = np.array_split(new_array, 8)

	split_array[data["x"]][data["y"]] = np.array(data["color"]).flatten()

	final = []

	for x in split_array:
		y = x.tolist()
		for item in y:
			final.append(item)

	with open("grid.csv", "w") as file:
		writer = csv.writer(file)

		for f in final:
			writer.writerow(f)

	sense.set_pixels(final)

	message = { "pixels": final }

	return jsonify(message)

@app.route("/data.json")
def get_data():
	return send_from_directory("get_weather/data/", "data.json")

@app.errorhandler(404) 
def not_found(error):
	return render_template("404.html"), 404

if __name__ == "__main__":
	app.run(host="0.0.0.0", debug=True)
