from collections import defaultdict        # <-- Structure the data into dictionary
from geopy.geocoders import Nominatim      # <-- Geolocator to make the API working
from datetime import datetime              # <-- Date & Time to import the current time in the user location
from requests import get                   # <-- Request library to get the API URL Working
from time import sleep                     # <-- Controle the time sleep in the program
from sys import exit                       # <-- Library use to exit the program when the user is done
from os import system                      # <-- Library use to clear the terminal
from timezonefinder import TimezoneFinder
from pytz import timezone


def get_api_data(BASE_URL, location, key_api):
    """Get the Air Quality API Data"""

    api = get(f"{BASE_URL}{location}/?token={key_api}")
    if api.status_code == 200:
        return api.json()
    return None

def get_timezone(zip_code):
    """Get the current time zone according to zip code"""

    geolocator = Nominatim(user_agent="MyGeoPy")
    location   = geolocator.geocode({'postalcode': int(zip_code)}) if zip_code.isnumeric() else 0
    timezone_finder = TimezoneFinder()

    result = timezone_finder.timezone_at(
        lng=location.longitude,
        lat=location.latitude)
        
    return datetime.now(timezone(result))

def get_location(zip_code):
    """Get the user location base on zip code"""
    
    try:
        geolocator = Nominatim(user_agent="MyGeoPy")
        postal     = geolocator.geocode({'postalcode': int(zip_code)}) if zip_code.isnumeric() else 0
        location   = f"{postal.latitude};{postal.longitude}"

    except:
        print("Sorry, based on your input, we were unable to collect any information from our database ...")
        exit(0)

    return location

def get_air_quality_info(time_zone, data):
    """Get Air Quality Informations Stored into Dictionary"""

    air_quality_info = defaultdict(list)
    current_time     = time_zone.strftime("%Y-%m-%d %H:%M")
    forecast         = get_forecast(data)

    air_quality_info['current_aqi']        = data['aqi']
    air_quality_info['current_pm25']       = data['iaqi']['pm25']['v']
    air_quality_info['dominant_pollutant'] = data['dominentpol']
    air_quality_info['current_city']       = data['city']['name']
    air_quality_info['current_time']       = current_time
    air_quality_info['ozone']              = forecast['o3']
    air_quality_info['pm_ten']             = forecast['pm10']
    air_quality_info['pm_twofive']         = forecast['pm25']
    air_quality_info['uvi']                = forecast['uvi']

    return air_quality_info

def get_forecast(data):
    """Get Forecast informations"""

    return data['forecast']['daily']

def get_forecast_info(forecast_element):
    """Get forecast for each Air Quality Element"""

    element = defaultdict(list)

    for forecast in range(len(forecast_element)):
        element['day']     += [forecast_element[forecast]['day']]
        element['average'] += [forecast_element[forecast]['avg']]
        element['max']     += [forecast_element[forecast]['max']]
        element['min']     += [forecast_element[forecast]['min']]

    return element

def display_air_quality_element(aq_info):
    """Display Air Quality Element Informations"""

    clear_console()
    for information in range(len(aq_info)):
        print(f"""
        Forecast Date -> {aq_info[information]['day']}
        Average Index -> {aq_info[information]['avg']}
        Max Index     -> {aq_info[information]['max']}
        Min Index     -> {aq_info[information]['min']}
        """)

    print("Press enter to return to air quality information!")
    input()

def fetch_forecast_air_quality(menu_option, air_quality_info):
    """Fetch Air Quality Forecast Informations"""
    
    if not (menu_option.isnumeric()):
        print("Enter Digit Only!")
        sleep(1)

    else:
        menu_option = int(menu_option)

        if menu_option == 1:
            return air_quality_info['pm_ten']
        
        elif menu_option == 2:
            return air_quality_info['pm_twofive']

        elif menu_option == 3:
            return air_quality_info['ozone']

        elif menu_option == 4:
            return air_quality_info['uvi']

        elif menu_option == 5:
            index_level()

        elif menu_option == 6:
            index_info()

        elif menu_option == 7:
            clear_console()
            print("Thanks for using our service.")
            exit(0)

        elif menu_option > 7 or menu_option < 1:
            print("Index number not available! Try another one.")
            sleep(2)

def index_info():
    """Explain the informations about the air quality"""
    clear_console()

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
    
def index_level():
    """Explain AQI, PMs and UV index level scale"""
    
    clear_console()

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

def clear_console():
    """Clear the console"""

    system("cls || clear")

    print("""
    \t\t\t _______________
    \t\t\t| AirQualityPy! |
    \t\t\t ---------------
    """)

def air_quality_menu(air_quality_info):
    """Display Current Air Quality Informations"""

    while True:
        clear_console()

        current_time      = air_quality_info['current_time']
        current_pollutant = air_quality_info['dominant_pollutant']
        current_aqi       = air_quality_info['current_aqi']
        current_pm25      = air_quality_info['current_pm25']
        current_city      = air_quality_info['current_city']
        
        print(f"""
        \tCurrent Date & Time         : {current_time}
        \tCurrent Dominant Pollutant  : {current_pollutant.upper()}
        \tCurrent Air Quality Index   : {current_aqi}
        \tCurrent PM2.5 value         : {current_pm25}
        \tAir Quality Station Location: {current_city}
        """)
        print(
            "\t\t1.[PM10] / 2.[PM2.5] / 3.[Ozone] / 4.[UV Index]\n\t5.[Index Level Scale] / 6.[Data Reference information] / 7.[Quit]")
        
        menu_option = input("\nWhich information do you want to access? [Index #]\n>>")
        aq_info     = fetch_forecast_air_quality(menu_option, air_quality_info)
        display_air_quality_element(aq_info) if type(aq_info) is list else aq_info

def main():
    """Main function of the program"""
    
    clear_console()

    key_api   = ""# --- your key API here --- # 
    BASE_URL  = "https://api.waqi.info/feed/geo:"

    zip_code  = input("Please, provide your zip code: ")
    location  = get_location(zip_code)
    time_zone = get_timezone(zip_code)
    api_data  = get_api_data(BASE_URL, location, key_api)

    if api_data:
        data = api_data['data']
        air_quality_info = get_air_quality_info(time_zone, data)
        air_quality_menu(air_quality_info)

    else:
        print("Air Quality Information No Found!")


if __name__ == "__main__":
    main()
