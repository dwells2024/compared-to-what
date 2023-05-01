# %%
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors

# %% [markdown]
# # Import and clean data

# %%
# import data
data = pd.read_csv('us_acs_qf_clean_density.csv')

# clean data
# remove index column since it doesn't provide valuable info
data = data.drop(["place_id"], axis = 1)
# remove state_id
data = data.drop(["state_id"], axis = 1)

# REMOVE NULL / BAD DATA

# remove city names for scaling
locations = data["Name"]
data = data.drop(["Name"], axis=1)

# standardize data
scaler = StandardScaler()
scaler.fit(data)
scaled_data = pd.DataFrame(scaler.transform(data), columns = data.columns)

# %% [markdown]
# # Add weights to model

# %%
no_weights = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
       1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
       1.0, 1.0, 1.0, 1.0, 1.0]
no_weights = pd.Series(no_weights)
data_no_weights = scaled_data.copy()

i = 0
for column in data_no_weights:
    data_no_weights[column] = data_no_weights[column].multiply(no_weights[i])
    i = i + 1 

data_no_weights.head()

# %%
pop_weights = [2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
       1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
       1.0, 1.0, 1.0, 1.0, 1.0]
pop_weights = pd.Series(pop_weights)
data_pop_weights = scaled_data.copy()

i = 0
for column in data_pop_weights:
    data_pop_weights[column] = data_pop_weights[column].multiply(pop_weights[i])
    i = i + 1 

data_pop_weights.head()

# %%
location_weights = [0.0, 0.5, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
       1.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
       1.0, 1.0, 1.0, 2.0, 2.0]
location_weights = pd.Series(location_weights)
data_location_weights = scaled_data.copy()

i = 0
for column in data_location_weights:
    data_location_weights[column] = data_location_weights[column].multiply(location_weights[i])
    i = i + 1 

data_location_weights.head()

# %%
distance_weights = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
                    1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
                    1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
                    1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0]
distance_weights = pd.Series(distance_weights)
data_distance_weights = scaled_data.copy()

i = 0
for column in data_distance_weights:
    data_distance_weights[column] = data_distance_weights[column].multiply(distance_weights[i])
    i = i + 1 

data_distance_weights.head()

# %%
age_weights = [1.0, 1.0, 1.0, 1.0, 1.0, 3.0, 3.0, 3.0, 1.0, 1.0,
                    1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
                    1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
                    1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0]
age_weights = pd.Series(age_weights)
data_age_weights = scaled_data.copy()

i = 0
for column in data_age_weights:
    data_age_weights[column] = data_age_weights[column].multiply(age_weights[i])
    i = i + 1 

data_age_weights.head()

# %%
scaled_data.columns
#5, 6, 7

# %% [markdown]
# ## Categories
# - No weights (data_no_weights)
# - Population (data_pop_weights)
# - Location
# - Distance (ie. far away)
# - Demographics (age)
# 
# - Demographics (race)
# - Housing
# - Education
# - Economics
# - Smart score (everything)

# %% [markdown]
# # Run KNN algorithm

# %%
nbrs = NearestNeighbors(n_neighbors=20,
                        algorithm="ball_tree").fit(data_distance_weights)
distances, indices = nbrs.kneighbors(data_distance_weights)

# %% [markdown]
# # Query a city

# %%
query = locations.str.contains("milwaukee(?i)")
query.index[query]

# %%
locations[15374]

# %%
for i in indices[4634]:
    print(locations[i])

# %%
for i in indices[20968]:
    print(locations[i])

# %%
for i in indices[2558]:
    print(locations[i])

# %%
for i in indices[4492]:
    print(locations[i])

# %%
for i in indices[20936]:
    print(locations[i])

# %%
for i in indices[3377]:
    print(locations[i])

# %%
query = locations.str.contains("the villa(?i)")
query.index[query]

# %% [markdown]
# # Export to JSON file

# %%
import json

# %%
indices

# %%
with open("100nn_cities.json", 'w') as file:
    json.dump(indices.tolist(), file)


