import json
from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def index():
	with open("get_weather/data/temperature_data.json") as file:
		data = json.load(file)

	return jsonify(data)

if __name__ == "__main__":
	app.run(host="0.0.0.0", debug=True)