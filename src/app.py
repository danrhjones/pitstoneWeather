from flask import Flask
from flask_swagger_ui import get_swaggerui_blueprint
from pitstone_weather.routes import routes

app = Flask(__name__)
app.register_blueprint(routes)

SWAGGER_URL = '/weather/swagger'
API_URL = '/static/swagger.yml'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)



