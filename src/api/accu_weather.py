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

    def get_weather(self, city: str) -> list[dict]:
        try:
            location = self.get_location(city)
        except Exception as e:
            raise APIFetchException(f"Город {city} не найден")

        url = f"/forecasts/v1/daily/5day/{location}"
        data = self.get(
            url=url,
            params={
                "apikey": self.token,
                "details": True,
                "metric": True,
            })

        try:
            forecasts = []
            for day in data.get("DailyForecasts", []):
                min_temperature = day.get("Temperature", {}).get("Minimum", {}).get("Value", 0)
                max_temperature = day.get("Temperature", {}).get("Maximum", {}).get("Value", 0)
                forecasts.append({
                    "date": day.get("Date"),
                    "temperature_avg": (min_temperature + max_temperature) / 2,
                    "temperature_min": min_temperature,
                    "temperature_max": max_temperature,
                })

            return forecasts
        except Exception:
            raise APIFetchException(f"не удалось распаковать данные от сервера")
