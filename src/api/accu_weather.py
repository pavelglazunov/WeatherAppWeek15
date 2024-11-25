from src.api.base import RequestBase
from src.api.interface import WeatherDataInterface, WeatherData
from src.exceptions import APIFetchException


class AccuWeatherApi(WeatherDataInterface, RequestBase):
    base_url = "http://dataservice.accuweather.com"

    def __init__(self, token: str):
        self.token = token
        super().__init__()

    def get_location(self, city: str) -> str:

        data = self.get(
            url="/locations/v1/cities/search",
            params={
                "apikey": self.token,
                "q": city,
                "details": True,
            }
        )
        return data[0].get("Key")

    def get_weather(self, city: str) -> WeatherData:
        try:
            location = self.get_location(city)
        except Exception:
            raise APIFetchException(f"Город {city} не найден")

        url = f"/forecasts/v1/hourly/1hour/{location}"
        data = self.get(
            url=url,
            params={
                "apikey": self.token,
                "details": True,
                "metric": True,
            })
        print(data)
        try:
            return WeatherData(
                temperature=data[0].get("Temperature", {}).get("Value", 0),
                humidity=data[0].get("RelativeHumidity", -1),
                winter_speed=data[0].get("Wind", {}).get("Speed", {}).get("Value", -1),
                rain_probability=data[0].get("RainProbability"),
            )
        except Exception:
            raise APIFetchException(f"не удалось распаковать данные от сервера")
