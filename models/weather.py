import os
import requests

from datetime import datetime


class Weather:

    def __init__(
        self,
        name="Unknown",
        temperature="Unknown",
        text="Unknown",
        icon_code=0,
        last_updated=datetime.now().strftime("%Y-%m-%d %H:%M"),
    ):
        icon_mapping = {
            1000: "☀️",
            1003: "🌤️",  # Partly Cloudy
            1006: "🌥️",  # Cloudy
            1009: "☁️",  # OverCast
            0: "",
        }
        self.name = name
        self.temperature = temperature
        self.text = text
        self.icon_code = icon_code
        self.icon = icon_mapping.get(self.icon_code, "")
        self.last_updated = last_updated

    def __repr__(self) -> str:
        return f"Weather[name: {self.name}, temperature: {self.temperature}, text: {self.text}, icon_code: {self.icon_code}, icon: {self.icon}]"


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
                icon_code=res_obj["current"]["condition"]["code"],
                last_updated=res_obj["current"]["last_updated"],
            )

        return Weather()
