import requests
import time
from datetime import datetime
import json
from config import API_KEY, CITIES

class WeatherAPI:
    def __init__(self):
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"
    
    def kelvin_to_celsius(self, kelvin):
        return round(kelvin - 273.15, 2)
    
    def fetch_weather_data(self):
        weather_data = []
        
        for city in CITIES:
            try:
                params = {
                    'q': f"{city},in",
                    'appid': API_KEY
                }
                response = requests.get(self.base_url, params=params)
                data = response.json()
                
                processed_data = {
                    'city': city,
                    'main': data['weather'][0]['main'],
                    'temp': self.kelvin_to_celsius(data['main']['temp']),
                    'feels_like': self.kelvin_to_celsius(data['main']['feels_like']),
                    'humidity': data['main']['humidity'],
                    'wind_speed': data['wind']['speed'],
                    'dt': data['dt'],
                    'timestamp': datetime.fromtimestamp(data['dt']).strftime('%Y-%m-%d %H:%M:%S')
                }
                weather_data.append(processed_data)
                
            except Exception as e:
                print(f"Error fetching data for {city}: {str(e)}")
        
        return weather_data