from asyncore import write
import json
import csv

labels = {
    "NAME": "Name",
    "place": "place_id",
    "state": "state_id",
    "DP02_0088E": "Total Population",
    "Density": "Density",
    "Land Area": "Land Area",
    "DP03_0062E": "Median Household Income",
    "DP03_0088E": "Per capita income",
    "DP05_0005PE": "Under 5yo %",
    "DP05_0019PE": "Under 18yo %",
    "DP05_0029PE": "Over 65yo %",
    "DP05_0003PE": "Female %",
    "DP05_0064PE": "White %",
    "DP05_0065PE": "Black or African American %",
    "DP05_0066PE": "American Indian and Alaska Native %",
    "DP05_0067PE": "Asian %",
    "DP05_0068PE": "Native Hawaiian and Other Pacific Islander %",
    "DP05_0035PE": "Two or more races %",
    "DP05_0071PE": "Hispanic or Latino %",
    "DP05_0077PE": "White alone, not Hispanic or Latino %",
    "DP02_0094PE": "Foreign born %",
    "DP04_0001E": "Total Housing Units",
    "DP04_0046E": "Owner-occupied Housing Units",
    "DP04_0089E": "Median value of owner-occupied housing units",
    "DP04_0101E": "Median selected monthly owner costs - with mortgage",
    "DP04_0109E": "Median selected monthly owner costs - without mortgage",
    "DP04_0134E": "Median gross rent",
    "DP02_0001E": "Total households",
    "DP02_0016E": "Persons per household",
    "DP02_0080PE": "Living in the same house 1 year ago %",
    "DP02_0114PE": "Language other than English spoken at home %",
    "DP02_0153PE": "Households with computer %",
    "DP02_0154PE": "Households with internet %",
    "DP02_0067PE": "High school graduate or higher %",
    "DP02_0068PE": "Bachelor's degree or higher %",
    "DP02_0076PE": "18-64yo with disability %",
    "DP03_0099PE": "Without health insurance %",
    "DP03_0002PE": "In labor force over 16yo %",
    "DP03_0011PE": "In labor force females over 16yo %",
    # "DP03_0025E": "Mean travel time to work (minutes)",
    "DP03_0128PE": "People in poverty %",
    "Latitude": "Latitude",
    "Longitude": "Longitude"
}

# with open("2021_Gaz_place_national.txt") as file:
#     datatable = [line.split() for line in file.read().splitlines()]

# with open("state_names.json") as file:
#     state_names = json.load(file)

with open("saved_data.json") as f:
    data = json.load(f)

# for gaz in datatable[1:]:
#     found = False
#     place_id = gaz[1]
#     # name = gaz[3]
#     # offset = 0
#     # for entry in gaz[4:]:
#     #     if not entry.isnumeric():
#     #         name = name + " " + entry
#     #         offset += 1
#     #     else:
#     #         break
#     # name = name + ', ' + state_names[gaz[0]]
#     # if gaz[0] != "PR":
#     #     for place in list(data.values())[1:]:
#     #         if place["NAME"] == name:
#     #             found = True
#     if place_id[0:2] != "72" and place_id in data:
#     #     found = True
#         place = data[place_id]
#         place["Land Area"] = gaz[-4]
#         place["Density"] = str(float(place["DP02_0088E"])/float(place["Land Area"]))
#         place["Latitude"] = gaz[-2]
#         place["Longitude"] = gaz[-1]
#     # if not found:
#     #     print(name)

# with open("saved_data.json", 'w') as f:
#     json.dump(data, f)

list_of_dicts = []
for place in list(data.values())[1:]:
    # print(list(place.values()))
    add = True
    if place["state"] == "72":
        add = False
    for data in list(place.values()):
        if data != None and data.strip('-').isnumeric():
            if float(data) <= -666666:
                add = False
    if add:
        # print("skip")
        list_of_dicts.append(place)

with open("us_acs_qf_clean_density.csv", 'w', newline='') as file:
    # writes to a csv file using dictionary format
    writer = csv.DictWriter(file, fieldnames=list(labels.keys()), restval='', extrasaction='ignore')

    # writes header
    writer.writerow(labels)

    # adds all rows
    writer.writerows(list_of_dicts)
