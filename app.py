from flask import Flask, request, jsonify
import os
# from flask_cors import CORS
import json


app = Flask(__name__)

# CORS: allows anyone from anywhere to use your API:
# cors = CORS(app)
with open("data/place_indices.json") as file:
	place_indices = json.load(file)

# @app.route("/", defaults={'path':''})
@app.route("/")
def default():
	return "<p>Compared to What API</p><p>Documentation coming soon</p>"

@app.route("/get-similar")
def get_similar_cities():
	place = request.args.get("place")
	if place == None:
		return "<p>You must specify a place. Refer to <a href=\"/\">comparedtowhat.azurewebsites.net</a> for examples."
	if place not in place_indices["places"]:
		return "Place not found. Make sure you are using the correct census place name and formatting. Refer to <a href=\"/\">comparedtowhat.azurewebsites.net</a> for examples."
	
	n = request.args.get("n")
	if n == None:
		n = 10
	elif n.isnumeric():
		n = int(n)
		if n > 100:
			return "<p>n must be an integer (max 100). Refer to <a href=\"/\">comparedtowhat.azurewebsites.net</a> for documentation."
	else:
		return "<p>n must be an integer (max 100). Refer to <a href=\"/\">comparedtowhat.azurewebsites.net</a> for documentation."
	
	filter = request.args.get("filter")
	if filter == None:
		filter = "smart_no_location"
	if filter + ".json" not in os.listdir("data/knns/"):
		return "<p>Filter not found. Click <a href=\"/filters\">here</a> for a list of all filters"
	path = "data/knns/" + filter + ".json"
	
	with open(path) as file:
		knn_cities = json.load(file)
	
	if type(knn_cities) == dict:
		indices_list = knn_cities["knn"]
	else:
		indices_list = knn_cities
	similar_cities_indices = indices_list[place_indices["places"][place]][1:n+1]
	similar_cities_names = [place_indices["indices"][str(index)] for index in similar_cities_indices]
	
	return similar_cities_names

@app.route("/all-places")
def get_places():
	return jsonify(list(place_indices["places"].keys()))

@app.route("/all-filters")
def get_filters():
	return jsonify([path[:-5] for path in os.listdir("data/knns/")])

@app.route("/filters")
def print_filters():
	return "".join(["<p>" + path[:-5] + "</p>" for path in os.listdir("data/knns/")])

@app.route("/filter-weights")
def filter_weights():
	filter = request.args.get("filter")
	if filter == None:
		return "you must specify a filter"
	
	path = "data/knns/" + filter + ".json"
	
	with open(path) as file:
		filter_json = json.load(file)

	html = "<table><tr><th>Metric</th><th>Weight</th></tr>"

	for i in range(len(filter_json["labels"])):
		html += "<tr><td>"
		html += filter_json["labels"][i]
		html += "</td><td>"
		html += str(filter_json["weights"][i])
		html += "</td></tr>"

	html += "</table>"

	return html

@app.route("/filter-description")
def filter_description():
	filter = request.args.get("filter")
	if filter == None:
		return "you must specify a filter"
	
	path = "data/knns/" + filter + ".json"
	
	with open(path) as file:
		filter_json = json.load(file)
	
	return "<p>" + filter_json["description"] + "</p><p>To see the weights for each metric click <a href=\"/filter-weights?filter=" + filter + "\">here</a>.</p>"

@app.route("/latlong")
def get_latlong():
	place = request.args.get("place")
	if place == None:
		return "<p>You must specify a place. Refer to <a href=\"/\">comparedtowhat.azurewebsites.net</a> for examples."
	if place not in place_indices["places"]:
		return "Place not found. Make sure you are using the correct census place name and formatting. Refer to <a href=\"comparedtowhat.azurewebsites.net\">comparedtowhat.azurewebsites.net</a> for examples."
	
	with open("data/latlongs.json") as file:
		data = json.load(file)
		return data[place]
