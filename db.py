from environs import Env
from flask import make_response, jsonify

from mongoengine import *

from pitstone_weather.hayfever import get_hayfever_for_today
from pitstone_weather.helpers import get_daily_weather
from models.hayfever import Hayfever
from models.weather import Weather

env = Env()
env.read_env()

client = connect(env('COLLECTION'), host=env('HOST'), port=env.int('PORT'))


def download_daily_stats(date):
    daily_stats = get_daily_weather(date)
    daily_stats_json = daily_stats.json()
    if daily_stats.status_code == 400:
        return make_response(
                jsonify(daily_stats_json['errors'][0]['message']), 400)
    else:
        for i in range(len(daily_stats_json["observations"])):
            observations = daily_stats_json["observations"][1]
            metric = observations['metric']
            weather = Weather(
                    stationID=observations["stationID"],
                    tz=observations["tz"],
                    obsTimeUtc=observations["obsTimeUtc"],
                    obsTimeLocal=observations["obsTimeLocal"],
                    epoch=observations["epoch"],
                    lat=observations["lat"],
                    lon=observations["lon"],
                    solarRadiationHigh=observations["solarRadiationHigh"],
                    uvHigh=observations["uvHigh"],
                    winddirAvg=observations["winddirAvg"],
                    humidityHigh=observations["humidityHigh"],
                    humidityLow=observations["humidityLow"],
                    humidityAvg=observations["humidityAvg"],
                    qcStatus=observations["qcStatus"],
                    tempHigh=metric["tempHigh"],
                    tempLow=metric["tempLow"],
                    tempAvg=metric["tempAvg"],
                    windspeedHigh=metric["windspeedHigh"],
                    windspeedLow=metric["windspeedLow"],
                    windspeedAvg=metric["windspeedAvg"],
                    windgustHigh=metric["windgustHigh"],
                    windgustLow=metric["windgustLow"],
                    windgustAvg=metric["windgustAvg"],
                    dewptHigh=metric["dewptHigh"],
                    dewptLow=metric["dewptLow"],
                    dewptAvg=metric["dewptAvg"],
                    windchillHigh=metric["windchillHigh"],
                    windchillLow=metric["windchillLow"],
                    windchillAvg=metric["windchillAvg"],
                    heatindexHigh=metric["heatindexHigh"],
                    heatindexLow=metric["heatindexLow"],
                    heatindexAvg=metric["heatindexAvg"],
                    pressureMax=metric["pressureMax"],
                    pressureMin=metric["pressureMin"],
                    pressureTrend=metric["pressureTrend"],
                    precipRate=metric["precipRate"],
                    precipTotal=metric["precipTotal"]
            )

            weather.save()

        return make_response(jsonify('Success!'), 200)


def download_daily_heyfever_stats():
    daily_stats = get_hayfever_for_today()
    daily_stats_json = daily_stats.json
    if daily_stats.status_code == 400:
        return make_response(jsonify('message'), 400)
    else:
        hayfever = Hayfever(
                day=daily_stats_json['day'],
                level=daily_stats_json['level'],
                message=daily_stats_json['message']
        )

        hayfever.save()
        return make_response(jsonify('Success!'), 200)
