"""
Данная апи использована для тестов, чтобы не тратить запросы на основой
"""
from src.api.base import RequestBase
from src.api.interface import WeatherDataInterface, WeatherData


class OpenWeatherApi(WeatherDataInterface, RequestBase):
    base_url = "https://api.openweathermap.org/data/2.5/weather"

    def __init__(self, token: str):
        self.token = token
        super().__init__()

    def get_weather(self, city: str) -> WeatherData:
        data = self.get("/", params={
            "q": city,
            "appid": self.token,
        })

        return WeatherData(
            temperature=data.get("main", {}).get("temp", 0) - 273.15,
            humidity=data.get("main", {}).get("humidity", -1),
            winter_speed=data.get("wind", {}).get("speed", -1),
            rain_probability=0,
        )
