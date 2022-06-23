# The program will provide different Air Quality information base on a zip code. 
# The informations are:
# The location of the monitoring station
# The dominant pollutant
# The current AQI(air quality index)
# Ozone, PM10, PM2.5, UV Index information for the current day, the previous two days, and a 5 day forecast
# Information includes average, min, and max
# Plus, category that explain the informations about the index scales.

'''Created by Chris Dedman-Rollet, 12/06/2021'''

# Import packtage needed
from geopy.geocoders import Nominatim       # <-- Geolocator to make the API working
from datetime import datetime               # <-- Date & Time to import the current time in the user location
import requests                             # <-- Request library to get the API URL Working
import json                                 # <-- Json library to extract data from json file
import time                                 # <-- Controle the time sleep in the program
import sys                                  # <-- Library use to exit the program when the user is done
import os                                   # <-- Library use to clear the terminal when move to different categories


# Extract weather informations from World Air Quality Index website, and store the datas into variables in json format
def data():
    # Global variable to be export the variable into different functions
    global pm_ten, pm_twofive, ozone, uvi, current_time, pollutant, aqi, current_pm25, current_city
    
    while True:
        geolocator = Nominatim(user_agent="MyGeoPy")
        keyAPI = "ENTER YOUR OWN TOKEM HERE"     # <-- TOKEN to make the API work from the website on the next line (waqi.info)
        url = "https://api.waqi.info/feed/geo:"
        # the user enter a zip code
        addr = input("Please, provide your zip code: ")

        # if the user entering a correct zip number, proceed gathering informations
        if (addr.isnumeric()):
            # Handle invalid zip code
            try:
                # geopy translate the zip code into cardinal point
                postal = geolocator.geocode({'postalcode': int(addr)})
                location = f"{postal.latitude};{postal.longitude}"
                # complete url for the API to proccess data
                complete_url = f"{url}{location}{keyAPI}"
                # the API get the data from the url
                response = requests.get(complete_url)
                x = response.json()  # the data are translate and store into the x variable in json format

                y = x['data']  # extract the json data and store it into a variable
                aqi = y['aqi']  # current Air Quality Index
                current_pm25 = y['iaqi']['pm25']['v']  # current PM2.5 index
                pollutant = y['dominentpol']  # current dominent pollutant
                current_city = y['city']['name']  # name of the current city
                current_time = y['time']['s'][:10]  # current_time[:9]
                ozone = y['forecast']['daily']['o3']  # prediction o3
                pm_ten = y['forecast']['daily']['pm10']  # prediction PM10
                pm_twofive = y['forecast']['daily']['pm25']  # prediction PM2.5
                uvi = y['forecast']['daily']['uvi']  # prediction UV index

                # break the while loop once the data are gathered, and move to the next function
                break

            # If zip code no found, print an error and start over.
            except (AttributeError, KeyError):
                print("Sorry, based on your input, we were unable to collect any information from our database ... \nPlease enter another zip code! \n")
                continue            

        # If the user do not enter a numerical zip code, print an error and start again.
        else:
            print('Invalid Input!\n')
            continue

# user menu to access different air quality informations
def air():
    os.system("cls||clear")
    print("""
    \t\t\t ________________________
    \t\t\t|Welcome to AirQualityPy!|
    """)
    # Gathered the current time
    now = datetime.now()
    time_now = now.strftime("%H:%M")

    # Print the user menu with different category option.
    print(f"\n\tCurrent Date & Time: {current_time} / {time_now}\n\tDominant pollutant: {pollutant}\n\tCurrent Air Quality Index: {aqi}\n\tCurrent PM2.5 value: {current_pm25}\n\tStation Location: {current_city}\n")
    print(
        "\t\t1.[PM10] / 2.[PM2.5] / 3.[Ozone] / 4.[UV Index]\n\t5.[Index Level Scale] / 6.[Data Reference information] / 7.[Quit]")

    # Main user navigation between categories
    request = input("\nWhich information do you want to access? [Index #]\n>>")

    # IF the user input a non digital number, print a warning and try again. Else, proceed to the category
    if not (request.isnumeric()):
        print("Digit Number Only!")
        time.sleep(1)

    else:
        # convert the request variable into integer
        request = int(request)

        # If the user chose the index number 1, move to the PM10 category
        if request == 1:
            pmten()
        
        # If the user chose the index number 2, move to the PM2.5 category
        elif request == 2:
            pmtwo()

        # If the user chose the index number 3, move to the Ozone category
        elif request == 3:
            oz()

        # If the user chose the index number 4, move to the UV category
        elif request == 4:
            uv()

        # If the user chose the index number 5, move to the Index Level category
        elif request == 5:
            index_level()

        # If the user chose the index number 6, move to the Index Level Information Meaning category
        elif request == 6:
            index_info()

        # If the user chose the index number 7, the program close
        elif request == 7:
            os.system("cls || clear")
            print("Thanks for using our service.")
            sys.exit(0)

        # If the user chose the index number higher than 7 or less than 1, print an our of index error
        elif request > 7 or request < 1:
            print("Index number not available! Try another one.")
            time.sleep(2)

# Category that explain the informations about the air quality
def index_info():
    os.system("cls||clear")
    print("Learn the meaning of ozone, particulate matter (PM) 10 and 2.5, and ultraviolet (UV) index information here.")

    # Block that explain what are the informations gathered in the program.
    print("""
    Ozone: It is a gas and is created when an O2 compound is joined by another oxygen particle,
                    becoming o3 - a compound of three oxygen particles.

    PM10 & PM2.5: Airborne particulate matter (PM) is not a single pollutant,but rather is a mixture
                    of many chemical species. Particles are defined by their diameter for air quality 
                    regulatory purposes. Those with a diameter of 10 microns or less (PM10) are inhalable 
                    into the lungs and can induce adverse health effects. Fine particulate matter 
                    is defined as particles that are 2.5 microns or less in diameter (PM2.5). 
                    Therefore, PM2.5 comprises a portion of PM10.

    UltraViolet (UV): The ultraviolet index, or UV index, is an international standard measurement 
                    of the strength of the sunburn-producing ultraviolet radiation at a particular 
                    place and time. It is primarily used in daily forecasts aimed at the general public, 
                    and is increasingly available as an hourly forecast as well. On this scale, 
                    1 signifies the lowest risk of overexposure and 11+ indicates the highest risk of overexposure.
    """)

    print("Press enter to return to air quality information!")
    input()
    
# Category with AQI, PMs and UV index level scale:
def index_level():
    os.system('cls||clear')

    # Ultraviolet Index Scale Meaning
    print("""
    \t\t ________________
    \t\t| UV Index Scale |
\t1 - 2  = Low                 (No protection required)
\t3 - 5  = Medium              (Protection required)
\t6 - 7  = Hight               (Protection required)
\t8 - 10 = Very Hight          (Extra protection required)
\t11+    = Extremely High      (Extra protection required)
    """)

    # Air Quality Index Scale Meaning
    print("""
    \t\t _________________________
    \t\t| Air Quality Index Scale |
\t0   - 50     = Good
\t51  - 100    = Moderate
\t101 - 150    = Unhealthy for Sensitive Groups
\t151 - 200    = Unhealthy
\t201 - 300    = Very Unhealthy
\t301 - Higher = Hazardous
    """)

    # PM2.5 Index Scale Meaning
    print("""
    \t\t ___________________________
    \t\t| PM2.5 Index Scale (µg/m³) |
\t0     - 12     = Good
\t12.1  - 35.4   = Moderate
\t34.5  - 55.4   = Unhealthy for Sensitive Groups
\t55.5  - 150.4  = Unhealthy
\t150.5 - 250.4  = Very Unhealthy
\t250.5 - Higher = Hazardous
    """)

    # PM10 Index Scale Meaning
    print("""
    \t\t __________________________
    \t\t| PM10 Index Scale (µg/m³) |
\t0   - 54     = Good
\t55  - 154    = Moderate
\t155 - 254    = Unhealthy for Sensitive Groups
\t255 - 354    = Unhealthy
\t355 - 424    = Very Unhealthy
\t425 - Higher = Hazardous
    """)

    print("Press enter to return to air quality information!")
    input()

# Forecast informations about Ozone with 2 days old and 4 day predictions
def oz():
    os.system("cls||clear")
    sum = 0
    print("\nForecast:\n")

    # In a loop, gathering the information for the ozone category
    for sum in range(0, len(ozone)):
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

    print("Press enter to return to air quality information!")
    input()

# Forecast informations about PM10 with 2 days old and 4 day predictions
def pmten():
    os.system("cls||clear")
    sum = 0
    print("Forecast:\n")

    # In a loop, gathering the information for the PM10 category
    for sum in range(0, len(pm_ten)):
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

    print("Press enter to return to air quality information!")
    input()

# Forecast informations about PM2.5 with 2 days old and 4 day predictions
def pmtwo():
    os.system("cls||clear")
    sum = 0
    print("Forecast:\n")

    # In a loop, gathering the information for the PM2.5 category
    for sum in range(0, len(pm_twofive)):
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

    print("Press enter to return to air quality information!")
    input()

# Forecast informations about UV Index with 2 days old and 4 day predictions
def uv():
    os.system("cls||clear")
    sum = 0
    print("Forecast:\n")

    # In a loop, gathering the information for the UV category
    for sum in range(0, len(uvi)):
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

    print("Press enter to return to air quality information!")
    input()

# Start the program
if __name__ == "__main__":
    os.system("cls || clear")
    print("""
    \t\t\t ________________________
    \t\t\t|Welcome to AirQualityPy!|
    """)
    data()
    while True:
        air()
