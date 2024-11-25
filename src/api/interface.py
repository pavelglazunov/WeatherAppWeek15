"""
Так на основном апи ограниченное кол-во запросов, было принять волевое решение
сделать интерфейсы и тестировать все на open weather, после чего просто поменять токен и ссылку
"""
from abc import ABCMeta, abstractmethod
from dataclasses import dataclass


@dataclass
class WeatherData:
    temperature: float
    humidity: float
    winter_speed: float
    rain_probability: float


class WeatherDataInterface:
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_weather(self, city: str) -> WeatherData:
        pass
