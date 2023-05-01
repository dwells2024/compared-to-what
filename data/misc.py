import csv
import json

place_list = []

with open("us_acs_qf_clean.csv") as csvfile:
    reader = csv.reader(csvfile)

    for row in reader:
        place_list.append(row)

place_dict = {
    "places": {},
    "indices": {}
}

for i in range(1, len(place_list)):
    place_dict["places"][place_list[i][0]] = i-1
    place_dict["indices"][i-1] = place_list[i][0]

with open("place_indices.json", 'w') as file:
    json.dump(place_dict, file)
