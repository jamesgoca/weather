import csv
import numpy as np
from sense_hat import SenseHat

sense = SenseHat()

data = {
		"x": 3,
		"y": 3,
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
		final.append(y)

print(final[0][0])

sense.set_pixels(final)

# split_array[data["x"]][data["y"]] = str(data["color"])

# with open("grid.csv", "w", newline="") as file:
# 	writer = csv.writer(file)
# 	writer.writerows(grid_rows)

# sense.set_pixels(grid_rows)

# message = { "grid": flattened_list }