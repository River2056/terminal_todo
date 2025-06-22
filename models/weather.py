import os
import requests


class Weather:

    def __init__(
        self, name="Unknown", temperature="Unknown", text="Unknown", icon="Unknown"
    ):
        self.name = name
        self.temperature = temperature
        self.text = text
        self.icon = icon

    def __repr__(self) -> str:
        return f"Weather[name: {self.name}, temperature: {self.temperature}, text: {self.text}, icon: {self.icon}]"


class WeatherManager:
    """
    A Weather Manager for fetching weather related info
    """

    def __init__(self, city="Taipei"):
        self.API_KEY = os.getenv("WEATHER_API_KEY")
        self.base_url = f"https://api.weatherapi.com/v1/current.json?key={self.API_KEY}&q={city}&aqi=no"

    def fetch_weather(self) -> Weather:
        res = requests.get(self.base_url)
        if res.ok:
            res_obj = res.json()
            return Weather(
                name=res_obj["location"]["name"],
                temperature=res_obj["current"]["temp_c"],
                text=res_obj["current"]["condition"]["text"],
                icon=res_obj["current"]["condition"]["icon"],
            )

        return Weather()
