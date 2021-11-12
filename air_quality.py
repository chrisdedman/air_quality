# The program will provide different Air Quality information
# base on a zip code. The information are:
# The location of the monitoring station
# The dominant pollutant
# The current AQI(air quality index)
# Ozone, PM10, PM2.5, UV Index information for the current day, the previous two days, and a 5 day forecast
# Information includes average, min, and max
import requests
import json
import os
from geopy.geocoders import Nominatim

def data():
    global current_time
    global current_pm25
    global current_city
    global aqi
    global pollutant
    global ozone
    global pm_ten
    global pm_twofive
    global uvi
    try:
        print("Welcome to AirQualityPy!")
        geolocator = Nominatim(user_agent="MyGeoPy")
        keyAPI = "/?token=dcc4b7d1eddc2abadd1f4bb8f9670815df7b0f20"
        url = "https://api.waqi.info/feed/geo:"
        # the user enter a zip code
        addr = int(input("Please, provide your zip code: "))
        # geopy translate the zip code into cardinal point
        postal = geolocator.geocode({'postalcode': addr})
        location = f"{postal.latitude};{postal.longitude}"
        # complete url for the API to proccess data
        complete_url = f"{url}{location}{keyAPI}"
        response = requests.get(complete_url)  # the API get the data from the url
        x = response.json()  # the data are translate and store into the x variable in json format

        y = x['data']  # extract data and store it into a variable
        aqi = y['aqi']  # current Air Quality Index
        current_pm25 = y['iaqi']['pm25']['v']  # current PM2.5 index
        pollutant = y['dominentpol']  # current dominent pollutant
        current_city = y['city']['name']  # name of the current city
        current_time = y['time']['s'][:10]  # current_time[:9]
        ozone = y['forecast']['daily']['o3']  # prediction o3
        pm_ten = y['forecast']['daily']['pm10']  # prediction PM10
        pm_twofive = y['forecast']['daily']['pm25']  # prediction PM2.5
        uvi = y['forecast']['daily']['uvi']  # prediction UV index
    except ValueError:
        print('Invalid Input!')

# Category with AQI index level scale:
def index_level():
    os.system('cls||clear')
    print("""
    \t\t\t ________________________
    \t\t\t| Air Quality Index Scale|

\t0   - 50  = Good
\t51  - 100 = Moderate
\t101 - 150 = Unhealthy for Sensitive Groups
\t151 - 200 = Unhealthy
\t201 - 300 = Very Unhealthy

    """)
    print("Press enter to go back to Air Quality Information!")
    input()
    air()

# user menu to access different air quality informations
def air():
    os.system("cls||clear")
    print("""
    \t\t\t ________________________
    \t\t\t|Welcome to AirQualityPy!|
    """)
    print(f"\n\tCurrent Date: {current_time}\n\tDominant pollutant: {pollutant}\n\tCurrent Air Quality Index: {aqi}\n\tCurrent PM2.5 value: {current_pm25}\n\tStation Location: {current_city}\n")
    print(
        "\t\t1.[PM10] / 2.[PM2.5] / 3.[Ozone] / 4.[UV Index]\n\t\t\t5.[Index Level Scale] / 6.[Quit]")

    try:
        request = int(
            input("\nWhich information do you want to access? [Index #]\n>>"))

        if request == 1:
            pmten()
        elif request == 2:
            pmtwo()
        elif request == 3:
            oz()
        elif request == 4:
            uv()
        elif request == 5:
            index_level()
        elif request == 6:
            exit(0)
        elif request > 6 or request < 1:
            return air() # <----------------------- need to work on this one, it should return request but I have a bug when I do so.

    except ValueError:
        air()

# Forecast informations about Ozone with 2 days old and 4 day predictions
def oz():
    os.system("cls||clear")
    sum = 0
    print("\nForecast:\n")
    while sum != len(ozone):
        for i in ozone[sum]['day']:
            print(i, end='')

        print("\nThe average Ozone is ", end='')
        for b in str(ozone[sum]['avg']):
            print(b, end='')

        print("\nThe max Ozone is ", end='')
        for c in str(ozone[sum]['max']):
            print(c, end='')

        print("\nThe min Ozone is ", end='')
        for d in str(ozone[sum]['avg']):
            print(d, end='')
        print("\n")
        sum += 1
    print("Press enter to access other Air Quality Information!")
    input()
    air()

# Forecast informations about PM10 with 2 days old and 4 day predictions
def pmten():
    os.system("cls||clear")
    sum = 0
    print("Forecast:\n")
    while sum != len(pm_ten):
        for i in pm_ten[sum]['day']:
            print(i, end='')

        print("\nThe average PM10 is ", end='')
        for b in str(pm_ten[sum]['avg']):
            print(b, end='')

        print("\nThe max PM10 is ", end='')
        for c in str(pm_ten[sum]['max']):
            print(c, end='')

        print("\nThe min PM10 is ", end='')
        for d in str(pm_ten[sum]['avg']):
            print(d, end='')
        print("\n")
        sum += 1
    print("Press enter to access other Air Quality Information!")
    input()
    air()

# Forecast informations about PM2.5 with 2 days old and 4 day predictions
def pmtwo():
    os.system("cls||clear")
    sum = 0
    print("Forecast:\n")
    while sum != len(pm_twofive):
        for i in pm_twofive[sum]['day']:
            print(i, end='')

        print("\nThe average PM2.5 is ", end='')
        for b in str(pm_twofive[sum]['avg']):
            print(b, end='')

        print("\nThe max PM2.5 is ", end='')
        for c in str(pm_twofive[sum]['max']):
            print(c, end='')

        print("\nThe min PM2.5 is ", end='')
        for d in str(pm_twofive[sum]['avg']):
            print(d, end='')
        print("\n")
        sum += 1
    print("Press enter to access other Air Quality Information!")
    input()
    air()

# Forecast informations about UV Index with 2 days old and 4 day predictions
def uv():
    os.system("cls||clear")
    sum = 0
    print("Forecast:\n")
    while sum != len(uvi):
        for i in uvi[sum]['day']:
            print(i, end='')

        print("\nThe average UV Index is ", end='')
        for b in str(uvi[sum]['avg']):
            print(b, end='')

        print("\nThe max UV Index is ", end='')
        for c in str(uvi[sum]['max']):
            print(c, end='')

        print("\nThe min UV Index is ", end='')
        for d in str(uvi[sum]['avg']):
            print(d, end='')
        print("\n")
        sum += 1
    print("Press enter to access other Air Quality Information!")
    input()
    air()


if __name__ == "__main__":
    while 1:
        data()
