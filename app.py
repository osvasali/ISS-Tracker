from flask import Flask, jsonify
from typing import List
import xmltodict, json, logging, socket

format_str = f'[%(asctime)s {socket.gethostname()}] %(filename)s:%(funcName)s:%(lineno)s - %(levelname)s: %(message)s'
logging.basicConfig(level=logging.DEBUG, format=format_str)
# error strings
output_error_str = '\nNo Data found! \n\nTo download, enter the following:\n  curl localhost:5027/download-data -X POST\n\n'
filenotfound_error_str = '\nFile not Found\n\n'

app = Flask(__name__)

# keys for the iss position data
epoch_key = 'EPOCH'

# keys from the sightings data
country_key = 'country'
region_key = 'region'
city_key = 'city'

@app.route('/', methods=['GET'])
def help():
    return '''\n-- How to Interact with this Application --\n
Start by dowloading data:
  curl localhost:5027/download -X POST\n
Use the following paths to acess the data:
  1.  /epochs
  2.  /epochs/<epoch>
  3.  /sightings
  4.  /sightings/countries
  5.  /sightings/<country>
  6.  /sightings/countries/regions
  7.  /sightings/<country>/regions
  8.  /sightings/region-<region>
  9.  /sightings/<country>-<region>-cities
  10. /sightings/city-<city>\n\n'''

@app.route('/download', methods=['POST'])
def download_data(iss_pos_filename = 'ISS.OEM_J2K_EPH.xml', sightings_filename = 'XMLsightingData_citiesUSA06.xml'):
    '''
    Loads the ISS position and sightings data from their respective XML files
    into the global variables iss_pos_data and sightings_data, respectively.
    '''
    try:
    global iss_pos_data, sightings_data
with open(iss_pos_filename, 'r') as f:
    data = xmltodict.parse(f.read())
iss_pos_data = data['ndm']['oem']['body']['segment']['data']['stateVector']
except FileNotFoundError as e:each dictionary is a sighting of the ISS
'''
try:
logging.debug('Get all sightings data queried')
return jsonify(sightings_data)
except Exception as e:
logging.error(e)
return output_error_str

@app.route('/sightings/countries', methods=['GET'])
def get_countries() -> List[dict]:
'''
Returns a list of dictionaries where each dicationary is a country
along with the numer of times a sighting occured in that country
'''
try:
countries = {}
sightings_countries = []
for sighting in sightings_data:
if sighting[country_key] in countries.keys():
countries[sighting[country_key]] += 1
else:
countries[sighting[country_key]] = 1

for country in countries.keys():
sightings_countries.append({'country': country, 'numsightings': countries[country]})
logging.debug('Get all countries queried')
return jsonify(sightings_countries)
except Exception as e:
logging.error(e)
return output_error_str


@app.route('/sightings/<country>')
def get_country(country: str) -> List[dict]:
'''
Takes in a country as user input and returns a list of dictionaries
where each dictionary is a sighting in that country
Args: 
country (str): the country the user would like to query
Returns:
country_data (list): a list of dictionaries containing all the sightings
data from that country (i.e. each dictionary in the list is a sighting).
'''
try:
country_data = []
for sighting in sightings_data:
if sighting[country_key] == country.title():
country_data.append(sighting)
logging.debug('Get specific country queried')
return jsonify(country_data)
except Exception as e:
logging.error(e)
return output_error_str

@app.route('/sightings/countries/regions', methods=['GET'])
def get_regions_of_countries() -> dict:
'''
Returns a dictionary where the keys are all of the countries in the sightings
data and the values are a list of the regions where a sighting occured in 
that country.
'''
try:
countries_regions = {}
for sighting in sightings_data:
if sighting[country_key] in countries_regions.keys():
if not (sighting[region_key] in countries_regions[sighting[country_key]]):
countries_regions[sighting[country_key]].append(sighting[region_key])
else:
countries_regions[sighting[country_key]] = [sighting[region_key]]
logging.debug('Get the regions of all countries queried')
return jsonify(countries_regions)
except Exception as e:
logging.error(e)
return output_error_str

@app.route('/sightings/<country>/regions', methods=['GET'])
def get_regions_of_country(country: str) -> dict:
'''
Takes in a country as user input and returns a dictionary where the first
and only key is the country given and the value is a list of dictionaries
where each dictionary is a region with the number of sightings within that
region.
Args:
country (str): the country the user would like to query
Returns:
A dictionary where they country is the first and only key and its value
is a list of dictionaries where each dictionary is a region within that
country where a sighting occured.
'''
try:
regions = {}
country_regions = []
for sighting in sightings_data:
if sighting[country_key] == country.title():
if sighting[region_key] in regions.keys():
regions[sighting[region_key]] += 1
else:
regions[sighting[region_key]] = 1
for region in regions.keys():
country_regions.append({'region': region, 'numsightings': regions[region]})
logging.debug('Get the regions of a specific country queried')
return jsonify({f'{country.title()}': country_regions})
except Exception as e:
logging.error(e)
return output_error_str

@app.route('/sightings/region-<region>', methods=['GET'])
def get_region(region: str) -> List[dict]:
'''
Takes in a region as user input and returns a list of dictionaries where wach dictionary is a sighting
in the region provided by the user.
Args:
region (str): the regions the user would to query
Returns:
region_sightings (list): a list of dictionaries where each dictionary
contains all the data from a sighting in the region
'''
try:
region_sightings = []
for sighting in sightings_data:
if sighting[region_key] == region.title():
region_sightings.append(sighting)
logging.debug('Get the data of a specific region queried')
return jsonify(region_sightings)
except Exception as e:
logging.error(e)
return output_error_str

@app.route('/sightings/<country>-<region>-cities')
def get_cities(country: str, region: str) -> dict:
'''
Takes a country and region as user input and returns a dictionary where the key is
the country provided and the value is another dictionary where the first key value-pair
is the region provided and the second key-value pair are the cities located in
that country and region
Args:
country (str): the country the user would like to query
region (str): the region the user would like to query
Returns:
Return a dictionary where the key is the country provided and the value is another dictionary 
where the first key value-pair is the region provided and the second key-value pair are the cities 
located in that country and region
'''
try:
cities = []
for sighting in sightings_data:
if (sighting[country_key] == country.title()) and (sighting[region_key] == region.title()):
if not (sighting[city_key] in cities):
cities.append(sighting[city_key])
logging.debug('Get the cities of a specific country and region queried')
return jsonify({country.title(): {'region': region.title(), 'citiesinregion': cities} })
except Exception as e:
logging.error(e)
return output_error_str

@app.route('/sightings/city-<city>', methods=['GET'])
def get_city(city: str) -> dict:
'''
Takes in a city name as user input and returns a dictionary where they key is
the city provided and the value is a list of all the data for sightings in that city
Args:
city (str): the city the user would like to query
Returns:
A dictionary where they key in the city name and the value is a list of dictionaries
where each dictionary contains all the data for a sighting in that city.
'''
try:
city_sightings = []
for sighting in sightings_data:
if sighting[city_key] == city.title():
city_sightings.append(sighting)
logging.debug('Get all the sighting data for a specific city queried')
return jsonify({city.title(): city_sightings})
except Exception as e:
logging.error(e)
return output_error_str

if __name__ == '__main__':
app.run(debug=True,host='0.0.0.0')
