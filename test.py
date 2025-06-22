import os
import requests
from dotenv import load_dotenv


def main():
    load_dotenv()

    API_KEY = os.getenv("WEATHER_API_KEY")
    base_url = (
        f"https://api.weatherapi.com/v1/current.json?key={API_KEY}&q=Taipei&aqi=no"
    )
    res = requests.get(url=base_url)
    if res.ok:
        res_obj = res.json()
        print(res_obj)
        print(res_obj["location"]["name"])
        print(res_obj["current"]["temp_c"])
        print(res_obj["current"]["condition"]["text"])
        print(res_obj["current"]["condition"]["icon"])


if __name__ == "__main__":
    main()
