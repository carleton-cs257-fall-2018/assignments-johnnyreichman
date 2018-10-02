#!/usr/bin/env python3
'''
    api-test.py
    Johnny Reichman, 1 October 2018

    This assignment recieves weather information from the OpenWeatherMap API

    There are two options for running the program:
    1)"python3 api-test.py weather zipcode" returns weather info for zipcode
    2)"python3 api-test.py heat latitude longitude" returns a list warm cities
                                            near location(between 0 and 10)
'''

import sys
import json
import urllib.request
import ssl


#returns the weather for a given zipcode
def get_weather(zipcode):
    base_url = 'http://api.openweathermap.org/data/2.5/weather?zip={0}&APPID=0fc28b9c445054ea35d60a41b1f111e9'
    url = base_url.format(zipcode)
    try:
        data_from_server = urllib.request.urlopen(url).read()
    except Exception as e:
        raise ValueError("Invalid zipcode",zipcode)
    string_from_server = data_from_server.decode('utf-8')
    fetched_list = json.loads(string_from_server)
    return fetched_list

#input a heat(fahrenheit) and latitude/longitude, 
#returns list of the closest cities with temperatures warmer than heat(0 to 10)
def get_hot_cities(heat, lat, lon):
    #converts heat from fahrenheit to kelvin(how it's stored in API)
    try:
        heat = float(heat)
        kelvin_heat = (heat+459.67)*5/9
    except Exception as e:
        raise TypeError("heat must be an float", heat)

    base_url = 'http://api.openweathermap.org/data/2.5/find?lat={0}&lon={1}&cnt=10&APPID=0fc28b9c445054ea35d60a41b1f111e9'
    url = base_url.format(lat, lon)

    try:
        data_from_server = urllib.request.urlopen(url).read()
    except Exception as e:
        raise ValueError("Invalid Latitude/Longitude",lat, lon)


    string_from_server = data_from_server.decode('utf-8')
    fetched_list = json.loads(string_from_server)
    all_cities = fetched_list["list"]
    hot_cities = []
    for city in all_cities:
        city_temp = city["main"]["temp"]
        if city_temp > kelvin_heat:
            hot_cities.append(city)

    return hot_cities


def main():
    if sys.argv[1] == "weather":
        if(len(sys.argv) != 3):
            print("Invalid number of args", len(sys.argv))
            quit()
        print(get_weather(sys.argv[2]))
    elif sys.argv[1] == "heat":
        if(len(sys.argv) != 5):
            print("Invalid number of args", len(sys.argv))
            quit()
        hot_cities = get_hot_cities(sys.argv[2], sys.argv[3], sys.argv[4])
        for city in hot_cities:
            print(city["name"])
    else:
        print("Invalid action, must be 'weather' or 'heat' ")



if __name__ == '__main__':

    main()