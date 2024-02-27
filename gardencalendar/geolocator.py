"""
B A S E    U R L 

base url for Nomatim API

https://nominatim.openstreetmap.org/search?<params>

amenity	| name and/or type of POI
street	| housenumber and streetname
city      | city
county    | county
state	| state
country	| country
postalcode| postal code

"""

import requests

def geocode(zip_code,country):

    base_url = "https://nominatim.openstreetmap.org/search"

    params = {

        'postalcode': zip_code,

        'country': country, 

        'format': 'json',

    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:

        data = response.json()

        if data:
            
            location = data[0]
            display_name= location['display_name']

            credit=location['licence']

            print(data)

            latitude, longitude = location['lat'], location['lon']

            return latitude, longitude,display_name,credit

        else:

            print("No results found.")

            return None

    else:

        print(f"Sorry! Something went wrong, please try again in a second: {response.status_code}")

        return None





"""
country='USA'
zip_code = input("Enter your zip code... ")
coords = geocode(zip_code,country)

print(coords)


if coords:
    location_info=coords[2].split(",")
    city_state=f"{location_info[0]}, {location_info[3]}"
    credit=coords[3]
    x=coords[0]
    y=[coords[1]]

    print(f"Your location is {city_state}")
       
    print(f"Latitude == {coords[0]}, Longitude == {coords[1]}")

    print(f"Geolocation done by--> {coords[3]}")

"""






