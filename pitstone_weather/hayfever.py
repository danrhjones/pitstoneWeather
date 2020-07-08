from datetime import datetime

import requests
from flask import jsonify
from selectolax.parser import HTMLParser


def get_hayfever_for_today():
    url = "https://www.metoffice.gov.uk/weather/warnings-and-advice/seasonal-advice/pollen-forecast"

    response = requests.get(url)

    message = {
        'day': datetime.now(),
        'level': HTMLParser(response.text.encode('utf8')).css_first("#se [data-type='pollen']").text(),
        'message': HTMLParser(response.text.encode('utf8')).css_first("#se-paras p").text()
    }

    return jsonify(message)
