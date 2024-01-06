import requests

import os

# Replace 'YOUR_TOKEN' with your actual NOAA API token

api_token = os.environ.get('NOAA')

x_coord = '40.7128'  # Example latitude

y_coord = '-74.0060'  # Example longitude



# NOAA API endpoint for Stations dataset

stations_url = 'https://www.ncdc.noaa.gov/cdo-web/api/v2/stations'



# Set up headers with your API token

headers = {'token': api_token}



# Set up parameters for the Stations API request

stations_params = {

    'limit': 1,

    'extent': f'{y_coord},{x_coord},{y_coord},{x_coord}',

}



# Make the Stations API request to get the closest station

stations_response = requests.get(stations_url, headers=headers, params=stations_params)

data=stations_response.json()
print(data)

#closest_station_id = stations_response.json()['results'][0]['id']



# NOAA API endpoint for Daily Summaries dataset
"""
daily_summaries_url = 'https://www.ncdc.noaa.gov/cdo-web/api/v2/data'



# Set up parameters for the Daily Summaries API request

daily_summaries_params = {

    'datasetid': 'GHCND',

    'datatypeid': 'TMAX',

    'limit': 1000,

    'startdate': '2022-01-01',

    'enddate': '2022-01-05',

    'stationid': closest_station_id,  # Use the closest station ID

    'units': 'metric',

}



# Make the Daily Summaries API request

daily_summaries_response = requests.get(daily_summaries_url, headers=headers, params=daily_summaries_params)



# Print the response

print(daily_summaries_response.json())

"""