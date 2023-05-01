import requests
import json

# define API variables
host_name = "https://api.census.gov/data/"
year = "2021/"
dataset = "acs/acs5/profile"
# year = "2017/"
# dataset = "ecnbasic"
key = "0082632a6b855e352235284fb3555ddcea5a98e4"

# select what variables to include

variables = ["NAME", "DP02_0088E", "DP03_0062E", "DP05_0005PE", "DP05_0019PE", "DP05_0029PE", "DP05_0003PE", "DP05_0064PE", "DP05_0065PE", "DP05_0066PE", "DP05_0067PE", "DP05_0068PE", "DP05_0035PE", "DP05_0071PE", "DP05_0077PE", "DP02_0094PE", "DP04_0001E", "DP04_0046E", "DP04_0089E", "DP04_0101E", "DP04_0109E", "DP04_0134E", "DP02_0001E", "DP02_0016E", "DP02_0080PE", "DP02_0114PE", "DP02_0153PE", "DP02_0154PE", "DP02_0067PE", "DP02_0068PE", "DP02_0076PE", "DP03_0099PE", "DP03_0002PE", "DP03_0011PE", "DP03_0025E", "DP03_0088E", "DP03_0128PE"] #acs5 data profiles
# variables = ["NAICS2017_LABEL", "NCAICS2017", "RCPTOT"]

# DC - 2020 Pop, 2010 Pop?
# Econ Cen - Accommodation and Food Services Sales, all other economy stuff

# select what predicates to include
# 10375,53000,24582,14000
predicates = ["for=place:*", "in=state:*"]

# combine variables into one url for API request
url = host_name + year + dataset + "?get=" + ','.join(variables) + '&' + '&'.join(predicates) + "&key=" + key
print(url)

# make the API request
response = requests.get(url)

# check if request failed
if response.status_code == 200:
    print("Success")
else:
    print(response.status_code)

with open("response.txt", 'w', encoding='utf-8') as f:
    f.write(response.text)

