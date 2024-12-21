from src.api.base import RequestBase
from src.api.interface import WeatherDataInterface
from src.exceptions import APIFetchException


class AccuWeatherApi(WeatherDataInterface, RequestBase):
    base_url = "http://dataservice.accuweather.com"

    def __init__(self, token: str):
        self.token = token
        super().__init__()

    def get_location(self, city: str) -> dict:

        data = self.get(
            url="/locations/v1/cities/search",
            params={
                "apikey": self.token,
                "q": city,
                "details": True,
            }
        )
        return data[0]

    def get_weather(self, city: str) -> list[dict]:
        try:
            location_data: dict = self.get_location(city)
        except Exception as e:
            raise APIFetchException(f"Город {city} не найден")

        url = f"/forecasts/v1/daily/5day/{location_data.get('Key')}"
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
                    "city": city,
                    "locations_lat": location_data.get("GeoPosition", {}).get("Latitude"),
                    "locations_lot": location_data.get("GeoPosition", {}).get("Longitude"),
                    "date": day.get("Date"),
                    "temperature_avg": (min_temperature + max_temperature) / 2,
                    "temperature_min": min_temperature,
                    "temperature_max": max_temperature,
                    "wind_speed": day.get("Day", {}).get("Wind", {}).get("Speed", {}).get("Value"),
                    "rain_probability": day.get("Day", {}).get("RainProbability"),
                    "humidity_min": day.get("Day", {}).get("RelativeHumidity", {}).get("Minimum",
                                                                                       0),
                    "humidity_max": day.get("Day", {}).get("RelativeHumidity", {}).get("Maximum",
                                                                                       0),
                    "humidity_avg": day.get("Day", {}).get("RelativeHumidity", {}).get("Average",
                                                                                       0),
                })
            return forecasts
        except Exception:
            raise APIFetchException(f"не удалось распаковать данные от сервера")
