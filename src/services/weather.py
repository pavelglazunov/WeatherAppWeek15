from src.api.interface import WeatherData


def check(weather_data: WeatherData) -> str:
    temperature_message = {
        "очень холодно": lambda x: x <= -30,
        "холодно": lambda x: -30 < x < 0,
        "есть признаки тепла": lambda x: 0 <= x < 20,
        "жарковато": lambda x: 20 <= x < 40,
        "До связи 🫡": lambda x: x >= 40,
    }

    humidity_message = {
        "можно сказать сухо": lambda x: 0 <= x <= 25,
        "чуть-чуть есть влаги": lambda x: 25 < x <= 50,
        "влаги чуть больше, чем чуть-чуть": lambda x: 50 < x < 75,
        "зато можно не поливать цветы, а то очень влажно": lambda x: 75 <= x <= 100,
    }

    winter_speed_message = {
        "на яхте не походим": lambda x: 0 <= x <= 5,
        "слегка ветрено": lambda x: 5 < x <= 20,
        "ждем Мэри Поппинс!": lambda x: x > 20,
    }
    rain_message = {
        "дождя скорее всего не будет": lambda x: x < 50,
        "пипяо, вероятность 50 на 50": lambda x: x == 50,
        "дождя скорее всего будет": lambda x: x > 50,
    }

    messages = [temperature_message, humidity_message, winter_speed_message, rain_message]

    message = []
    for msg, value in zip(messages, list(weather_data.__dict__.values())):
        for text, func in msg.items():
            if func(value):
                message.append(text)

    return ", ".join(message)
