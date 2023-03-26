from googletrans import Translator
import requests, json

def weather(city, API_KEY):
    translator = Translator()
    BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
    URL = BASE_URL + "q=" + city + "&appid=" + API_KEY
    response = requests.get(URL)
    if response.status_code == 200:
        data = response.json()
        weathers = translator.translate(text=data['weather'][0]['description'], dest='ru').text
        temperature = int(data['main']['temp'] - 273.15)
        wind = str(data['wind']['speed'])
        feel_like = int(data['main']['feels_like'] - 273.15)
        temp_min = int(data['main']['temp_min'] - 273.15)
        date=[weathers,temperature, wind, feel_like, temp_min]
        return date
    else:
        print("Error in HTTP request")