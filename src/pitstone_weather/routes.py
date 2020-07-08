from datetime import timedelta, datetime

from environs import Env
from flask import Blueprint, request, make_response, jsonify

from pitstone_weather.hayfever import get_hayfever_for_today
from pitstone_weather.helpers import get_current_stats, get_daily_stats
from db import download_daily_stats, download_daily_heyfever_stats

routes = Blueprint('route', __name__)
env = Env()
env.read_env()


@routes.route('/history/download', methods=['PUT'])
def download_all_history():
    if env("ALLOW_DOWNLOAD_FROM_WUNDERGROUND") == 'True':
        format_str = '%Y, %m, %d'
        start_date = datetime.strptime(request.json['start_date'], format_str)
        end_date = datetime.strptime(request.json['end_date'], format_str)

        if end_date > start_date:
            def date_range(start_date, end_date):
                for n in range(int((end_date - start_date).days)):
                    yield start_date + timedelta(n)

            for num, single_date in enumerate(date_range(start_date, end_date)):
                print('in loop')
                download_daily_stats(single_date.strftime("%Y%m%d"))

        elif start_date == end_date:
            print('in single')
            download_daily_stats(start_date.strftime("%Y%m%d"))

        return make_response(jsonify("History uploaded"), 200)
    else:
        return make_response(jsonify("Nothing to see here"), 404)


@routes.route('/hayfever')
def get_hayfever_levels():
    return get_hayfever_for_today()


@routes.route('/hayfever/download')
def download_hayfever_levels():
    return download_daily_heyfever_stats()


@routes.route('/weather/now', methods=['GET'])
def get_weather_now():
    if request.args.get('units') not in ['e', 'm', 'h']:
        return make_response(jsonify("units are incorrect"), 400)
    else:
        units = request.args.get('units')
        return make_response(get_current_stats(units), 200)


@routes.route('/weather/today', methods=['GET'])
def get_weather_today():
    if request.args.get('units') not in ['e', 'm', 'h']:
        return make_response(jsonify("units are incorrect"), 400)
    else:
        units = request.args.get('units')

        return make_response(get_daily_stats(units), 200)
