# %%
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors

# %%
# import data
data = pd.read_csv('data/us_acs_qf_clean.csv')

# %%
# clean data
# remove index column since it doesn't provide valuable info
data = data.drop(["place_id"], axis = 1)
# remove state_id for IL dataset
# data = data.drop(["state_id"], axis = 1)

# REMOVE NULL / BAD DATA

# remove city names for scaling
locations = data["Name"]
data = data.drop(["Name"], axis=1)


# %%
# standardize data
scaler = StandardScaler()
scaler.fit(data)
scaled_data = pd.DataFrame(scaler.transform(data), columns = data.columns)

# %%
scaled_data

# %%
nbrs = NearestNeighbors(n_neighbors=100,
                        algorithm="ball_tree").fit(scaled_data)
distances, indices = nbrs.kneighbors(scaled_data)

# %%
indices
# put array into json file for 100 nearest


# %%
distances

# %%
for i in indices[4634]:
    print(locations[i])

# %%
locations

# %%
query = locations.str.contains("Evanston")
query.index[query]

# %%
locations[4634]

# %%
import json

# %%
indices

# %%
with open("100nn_cities.json", 'w') as file:
    json.dump(indices.tolist(), file)

# %%



