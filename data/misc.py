import csv
import json

# place_list = []

# with open("us_acs_qf_clean.csv") as csvfile:
#     reader = csv.reader(csvfile)

#     for row in reader:
#         place_list.append(row)

# place_dict = {
#     "places": {},
#     "indices": {}
# }

# for i in range(1, len(place_list)):
#     place_dict["places"][place_list[i][0]] = i-1
#     place_dict["indices"][i-1] = place_list[i][0]

# with open("place_indices.json", 'w') as file:
#     json.dump(place_dict, file)

with open("saved_data.json") as file:
    data = json.load(file)

latlongs = {}

for place in list(data.values())[1:]:
    latlongs[place["NAME"]] = [float(place["Latitude"]), float(place["Longitude"])]

with open("latlongs.json", 'w') as file:
    json.dump(latlongs, file)
