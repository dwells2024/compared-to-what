from flask import Flask, request, jsonify
from flask_cors import CORS
import json
app = Flask(__name__)

# CORS: allows anyone from anywhere to use your API:
cors = CORS(app)
with open("data/place_indices.json") as file:
	place_indices = json.load(file)

with open("data/100nn_cities.json") as file:
	knn_cities = json.load(file)

@app.route("/all-places")
def get_places():
	return jsonify(list(place_indices["places"].keys()))

@app.route("/get-similar")
def get_similar_cities():
	place = request.args.get("place")
	similar_cities_indices = knn_cities[place_indices["places"][place]][1:11]
	similar_cities_names = [place_indices["indices"][str(index)] for index in similar_cities_indices]
	return similar_cities_names
