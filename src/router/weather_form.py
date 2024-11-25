import os

from flask import Blueprint, render_template, request

from config.config import Config
from src.api import AccuWeatherApi, OpenWeatherApi
from src.exceptions import APIFetchException
from src.services import weather

template_folder = os.path.join(os.getcwd(), "src", "templates")
router = Blueprint("weather", __name__, url_prefix="/weather", template_folder=template_folder)


@router.route("/", methods=["GET"])
def weather_page():
    return render_template("index.html")


@router.route("/", methods=["POST"])
def get_weather():
    config: Config = request.environ.get("config")
    api = AccuWeatherApi(config.api.key)
    # api = OpenWeatherApi(config.api.key)
    try:
        from_city_weather = api.get_weather(request.form.get("from_city"))
        from_city_text = weather.check(from_city_weather)
    except APIFetchException as e:
        from_city_text = e.message

    try:
        to_city_weather = api.get_weather(request.form.get("to_city"))
        to_city_text = weather.check(to_city_weather)
    except APIFetchException as e:
        to_city_text = e.message

    return render_template(
        "index.html",
        from_city_name=request.form.get("from_city"),
        to_city_name=request.form.get("to_city"),
        from_city_text=from_city_text,
        to_city_text=to_city_text,
    )
