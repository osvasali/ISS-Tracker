from flask import Flask, jsonify
from typing import List
import xmltodict, json, logging, socket

format_str = '%(levelname)s: %(message)s'
logging.basicConfig(level=logging.DEBUG, format=format_str)
app = Flask(__name__)

iss_positions = {}
iss_sightings = {}
error_string = "ERROR - DATA NOT FOUND - Use /help for more information\n"

@app.route('/help', methods=['GET'])
def help():
    '''
    Information on how to interact with the application

    Returns: A string describing what paths to use for each function.
    '''
    return '''\nFIRST LOAD DATA USING THE FOLLOWING PATH: /load -X POST\n
    IF THERE ARE ERROR LOAD THE DATA ONCE MORE\n\n
    Navigation:\n
    Use the following routes to access the data:
      1.  /epochs
          #lists all epochs
      2.  /epochs/<epoch>
          #data for specific epoch
      3.  /countries
          #lists all countries
      4.  /countries/<country>
          #data for specific country
      5.  /countries/<country>/regions
          #lists all regions
      6.  /countries/<country>/regions/<regions>
          #data for specific region
      7.  /countries/<country>/regions/<regions>/cities
          #lists all cities
      8. /countries/<country>/regions/<regions>/cities/<cities>
          #data for specific city\n\n'''

@app.route('/load', methods=['POST'])
def load():
    """
    Loads the ISS position and sightings data into global variables.

    Returns: string describing if data was loaded successfully or not
    """
    try:
        logging.info("Loading Positions Data.")
        global iss_positions
        with open('ISS.OEM_J2K_EPH.xml' , 'r') as f:
             iss_positions =  xmltodict.parse(f.read())
    except FileNotFoundError as e:
        logging.error(e)
        return 'POSITION DATA FILE NOT FOUND\n'

    try:
        logging.info("Loading Sightings Data.")
        global iss_sightings
        with open('XMLsightingData_citiesUSA06.xml' , 'r') as f:
             iss_sightings = xmltodict.parse(f.read())
    except FileNotFoundError as e:
        logging.error(e)
        return 'SIGHTINGS DATA FILE NOT FOUND\n'

    return f'Data has been loaded\n'

@app.route('/epochs', methods=['GET'])
def get_epochs():
    """
    Reads the data in the global variable iss_positions to create a new dictionary of epochs.

    Returns: a string of epoch dictionaries. An error if data is not found.
    """
    try:
        logging.info("Getting list of epochs...")
        epochs = ""
        for i in range(len(iss_positions['ndm']['oem']['body']['segment']['data']['stateVector'])):
            epochs = epochs + iss_positions['ndm']['oem']['body']['segment']['data']['stateVector'][i]['EPOCH'] + '\n'
        return epochs
    except Exception as e:
        logging.error(e)
        return error_string

@app.route('/epochs/<epoch>', methods=['GET'])
def get_epoch(epoch: str):
    '''
    Reads the data in the global variable iss_positions to create a dictionary for a specific epoch

    Parameters: <epoch> (str): an epoch name as a string variable
    Returns: A dictionary for an epoch that mathces the value. An error is returned if there is no match.
    '''
    try:
        logging.info("Loading data for the following epoch /"+epoch)
        xyz = ['X', 'Y', 'Z', 'X_DOT', 'Y_DOT', 'Z_DOT']
        epoch_data = {}
        for i in range(len(iss_positions['ndm']['oem']['body']['segment']['data']['stateVector'])):
            if epoch == iss_positions['ndm']['oem']['body']['segment']['data']['stateVector'][i]['EPOCH']:
                break
            for j in xyz:
                epoch_data[j] = iss_positions['ndm']['oem']['body']['segment']['data']['stateVector'][i][j]
            return epoch_data
    except Exception as e:
        logging.error(e)
        return error_string

@app.route('/countries',methods=['GET'])
def list_countries():
    """
    Reads the data in the global variable iss_sightings to create a new dictionary of countries.

    Returns: A dictionary of country dictionaries where each dictionary is the country the ISS was sighted in.
             An error if data is not found.
    """
    try:
        logging.info("Getting list of countries with sightings...")
        countries = {}
        j=0
        for i in range(len(iss_sightings['visible_passes']['visible_pass'])):
            iCountry = iss_sightings['visible_passes']['visible_pass'][i]['country']
            if iCountry in countries:
                countries[iCountry] += 1
            else:
                j+=1
                countries[iCountry] = 1
        return f'\n --Sightings per Country--\n\n' + json.dumps(countries, indent=2) + f'\n\n There are {j} countries with sightings found\n\n'
    except Exception as e:
        logging.error(e)
        return error_string

@app.route('/countries/<country>', methods=['GET'])
def country_data(country):
    """
    Reads the data in the global variable iss_sightings to create a dictionary for a specific country

    Parameters: <country> (str): a country name as a string variable
    Returns: A list that matches the value. An error is returned if there is no match.
    """

    try:
        logging.info("Getting data for the following country: /"+country)
        countries = []
        country_list = ['region', 'city', 'spacecraft', 'sighting_date','duration_minutes','max_elevation','enters','exits','utc_offset','utc_time', 'utc_date']
        for i in range(len(iss_sightings['visible_passes']['visible_pass'])):
            iCountry = iss_sightings['visible_passes']['visible_pass'][i]['country']
            if country == iCountry:
                country_data = {}
                for j in country_list:
                    country_data[j] = iss_sightings['visible_passes']['visible_pass'][i][j]
                countries.append(country_data)
        return json.dumps(countries, indent=2) + '\n\n'
    except Exception as e:
        logging.error(e)
        return error_string

@app.route('/countries/<country>/regions',methods=['GET'])
def list_regions(country):
    """
    Reads the data in the global variable iss_sightings to create a dictionary of regions

    Parameters: <country> (str): a country name as a string variable
    Returns: A dictionary of regions that mathces the value. An error is returned if there is no match.
    """
    try:
        logging.info("Getting list of regions in the following country: /"+country)
        regions = {}
        j = 0
        for i in range(len(iss_sightings['visible_passes']['visible_pass'])):
            iCountry = iss_sightings['visible_passes']['visible_pass'][i]['country']
            if country == iCountry:
                iRegion = iss_sightings['visible_passes']['visible_pass'][i]['region']
                if iRegion in regions:
                    regions[iRegion] += 1
                else:
                    regions[iRegion] = 1
                    j+=1
        return '\n--Sightings per Region--\n\n' + json.dumps(regions, indent=2) + f'\n\n There are {j} regions with sightings in {country}\n\n'
    except Exception as e:
        logging.error(e)
        return error_string

@app.route('/countries/<country>/regions/<region>',methods=['GET'])
def region_data(country: str, region: str) -> str:
    """
    Reads the data in the global variable iss_sightings to create a dictionary for a specific region

    Parameters: <country> (str): a country name as a string variable
                <region> (str): a region name as a string variable
    Returns: A dictionary for a region that mathces the <region> value. An error is returned if there is no match.
    """
    try:
        logging.info("Getting data for the following region: /"+region)
        region_data_dictionary  = {}
        country_data_dictionary = json.loads(country_data(country))
        region_list = []
        for i in country_data_dictionary:
            if (region == i['region']):
                del i["region"]
                region_list.append(i)
        region_data_dictionary[f'{region}'] = region_list
        return (json.dumps(region_data_dictionary,indent=2) + '\n\n')
    except Exception as e:
        logging.error(e)
        return error_string

@app.route('/countries/<country>/regions/<region>/cities',methods=['GET'])
def list_cities(country, region):
    """
    Reads the data in the global variable iss_sightings to create a dictionary of cities in a specific region

    Parameters: <country> (str): a country name as a string variable
                <region> (str): a region name as a string variable
    Returns: A list of cities in a region that mathces the <region> value. An error is returned if there is no match.
    """
    try:
        logging.info("Getting list of cities in the following region: /"+region)
        cities_data_dictionary = {}
        j = 0
        region_data_dictionary = json.loads(region_data(country, region))
        for i in region_data_dictionary[f'{region}']:
            if i['city'] not in cities_data_dictionary.values():
                    j += 1
            cities_data_dictionary[f'city {j}'] = i[f'city']
        return '\n--Cities with Sightings--\n\n' + (json.dumps(cities_data_dictionary, indent=2) + f'\n\n There are {j} cities with sightings in {region}\n\n')
    except Exception as e:
        logging.error(e)
        return error_string

@app.route('/countries/<country>/regions/<region>/cities/<city>',methods=['GET'])
def city_data(country, region, city):
    """
    Reads the data in the global variable iss_sightings to create a dictionary to create a dictionary for a specific city

    Parameters: <country> (str): a country name as a string variable
                <region> (str): a region name as a string variable
                <city> (str): a city name as a string variable
    Returns: A dictionary for a city that mathces the <city> value. An error is returned if there is no match.
    """
    try:
        logging.info('Getting data for the following city: /'+city)
        city_data_dictionary  = {}
        region_data_dictionary = json.loads(region_data(country, region))
        city_list = []
        j=0
        for i in region_data_dictionary[f'{region}']:
            if (city == i['city']):
                del i['city']
                city_list.append(i)
                j+=1
        city_data_dictionary[f'{city}'] = city_list
        return (json.dumps(city_data_dictionary,indent=2) + f'\n\n{j} sightings found in {city} \n\n')
    except Exception as e:
        logging.error(e)
        return error_string

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
