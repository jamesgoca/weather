import json
import pyowm
import os
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template

load_dotenv()

app = Flask(__name__)
owm = pyowm.OWM(os.environ.get("pyowm-key"))

@app.route("/")
def index():
	with open("get_weather/data/data.json") as file:
		data = json.load(file)

	forecast = owm.daily_forecast('london,uk')

	weather = forecast.get_weather_at(datetime.datetime.now())

	description = weather.get_detailed_status()

	return render_template("index.html", current_temp=data[-1], description=description)

if __name__ == "__main__":
	app.run(host="0.0.0.0", debug=True)