from datetime import datetime
import requests
from environs import Env

env = Env()
env.read_env()


def get_units(x):
    return {
        'm': 'metric',
        'h': 'uk_hybrid',
        'e': 'imperial'
    }.get(x, "error")


def get_current_stats(units):
    data = get_current_weather(units)
    return {
        "units": get_units(units),
        "localTime": data["observations"][0]["obsTimeLocal"],
        "temp": data["observations"][0][get_units(units)]["temp"],
        "humidity": data["observations"][0]["humidity"],
        "dewPoint": data["observations"][0][get_units(units)]["dewpt"],
        "heatIndex": data["observations"][0][get_units(units)]["heatIndex"],
        "windChill": data["observations"][0][get_units(units)]["windChill"],
        "windSpeed": data["observations"][0][get_units(units)]["windSpeed"],
        "windGust": data["observations"][0][get_units(units)]["windGust"],
        "pressure": data["observations"][0][get_units(units)]["pressure"],
        "precipitationRate": data["observations"][0][get_units(units)]["precipRate"],
        "precipitationTotal": data["observations"][0][get_units(units)]["precipTotal"]
    }


def get_daily_stats(units):
    data = get_daily_weather(units)
    return {
        "units": get_units(units),
        "windGustHigh": data["observations"][0][get_units(units)]["windgustHigh"],
        "tempAvg": data["observations"][0][get_units(units)]["tempAvg"],
        "tempLow": data["observations"][0][get_units(units)]["tempLow"],
        "tempHigh": data["observations"][0][get_units(units)]["tempHigh"]
    }


def get_daily_weather(units):
    url = "https://api.weather.com/v2/pws/history/daily"

    params = {
        'apiKey': env("API_KEY"),
        'stationId': env("STATION_ID"),
        'numericPrecision': 'decimal',
        'format': 'json',
        'units': units,
        'date': datetime.now().strftime('%Y%m%d')
    }

    response = requests.get(url, params=params)
    return response.json()


def get_current_weather(units):
    url = "https://api.weather.com/v2/pws/observations/current"

    params = {
        'apiKey': env("API_KEY"),
        'stationId': env("STATION_ID"),
        'numericPrecision': 'decimal',
        'format': 'json',
        'units': units
    }

    response = requests.get(url, params=params)
    return response.json()
