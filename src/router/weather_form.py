import os

from flask import Blueprint, render_template, request

template_folder = os.path.join(os.getcwd(), "src", "templates")
router = Blueprint("weather", __name__, url_prefix="/weather", template_folder=template_folder)


@router.route("/", methods=["GET"])
def weather_page():
    return render_template("index.html")


@router.route("/", methods=["POST"])
def get_weather():
    ...
    return render_template("index.html")
