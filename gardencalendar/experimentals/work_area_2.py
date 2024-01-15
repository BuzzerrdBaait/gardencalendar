import requests

from time import sleep



def get_weather(latitude, longitude):

    base_url = f"https://api.weather.gov/points/{latitude},{longitude}"

    response = requests.get(base_url)

    if response.status_code == 200:

        forecast_url = response.json()["properties"]["forecast"]

        forecast_response = requests.get(forecast_url)

        
        if forecast_response.status_code == 200:

            forecast_data = forecast_response.json()

            return forecast_data

        else:

            print(f"I failed to retreive the weather master. I am sorry that I failed you: {forecast_response.status_code}")
            sleep(1.5)
            print("BAD! Bad intelligence!  *rubs nose in shit*")
    else:

        print(f"Failure upon entering your point data. Did you enter a real point?: {response.status_code}")

    return None



latitude = 33.66110656785714  

longitude = -95.38478078928571

forecast = get_weather(latitude, longitude)



if forecast:

    for period in forecast["properties"]["periods"]:
        
        print(f"Date: {period['startTime']} - {period['endTime']}")

        print(f"Temperature: {period['temperature']} °F")

        print(f"Description: {period['shortForecast']}")

        print("\n")

        sleep(1.5)

        print(period)
