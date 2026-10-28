import requests
import json

import time
import requests


def check_api_key_status(api_key):
    """Check if your API key is active"""
    test_url = "https://api.openweathermap.org/data/2.5/weather"

    params = {
        "q": "London",
        "appid": api_key
    }

    response = requests.get(test_url, params=params)
    data = response.json()

    if data.get("cod") == 200:
        print("✅ API Key is working!")
        return True
    elif data.get("cod") == 401:
        print("❌ Invalid API key")
        print("Wait 10-30 minutes after signup for activation")
        return False
    else:
        print(f"Status: {data.get('message', 'Unknown error')}")
        return False


# Wait and retry if needed
API_KEY = "2cf30302348a84e6b2b34a405dca2d58"  # Get from signing up
for i in range(6):  # Try for 1 hour
    if check_api_key_status(API_KEY):
        break
    else:
        print(f"Waiting 10 minutes... ({i+1}/6 attempts)")
        time.sleep(600)  # Wait 10 minutes


def get_weather_by_coordinates(latitude, longitude):
    """
    Fetch weather data using latitude and longitude coordinates
    Free OpenWeatherMap API - No credit card needed
    Sign up at: https://openweathermap.org/api
    Free plan gives you 1,000 calls/day
    """
    API_KEY = "2cf30302348a84e6b2b34a405dca2d58"  # Replace with your OpenWeatherMap API key
    BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

    params = {
        "lat": latitude,
        "lon": longitude,
        "appid": API_KEY,
        "units": "metric"  # For Celsius, use "imperial" for Fahrenheit
    }

    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
        data = response.json()

        if data.get("cod") == 200:
            weather_info = {
                "city": data["name"],
                "country": data["sys"]["country"],
                "latitude": latitude,
                "longitude": longitude,
                "temperature": data["main"]["temp"],
                "feels_like": data["main"]["feels_like"],
                "humidity": data["main"]["humidity"],
                "pressure": data["main"]["pressure"],
                "wind_speed": data["wind"]["speed"],
                "wind_direction": data["wind"].get("deg", "N/A"),  # Wind direction in degrees
                "weather": data["weather"][0]["description"],
                "weather_main": data["weather"][0]["main"],  # Main weather category
                "icon": data["weather"][0]["icon"],  # For weather icons
                "visibility": data.get("visibility", "N/A"),  # Visibility in meters
                "cloudiness": data.get("clouds", {}).get("all", "N/A"),  # Cloudiness percentage
                "sunrise": data["sys"]["sunrise"],  # Unix timestamp
                "sunset": data["sys"]["sunset"],  # Unix timestamp
                "timezone": data.get("timezone", "N/A")  # Shift in seconds from UTC
            }

            # Convert Unix timestamps to readable format
            from datetime import datetime
            weather_info["sunrise_time"] = datetime.fromtimestamp(weather_info["sunrise"]).strftime('%H:%M:%S')
            weather_info["sunset_time"] = datetime.fromtimestamp(weather_info["sunset"]).strftime('%H:%M:%S')

            print(f"Weather at Coordinates ({latitude}, {longitude}):")
            print(f"📍 Nearest City: {weather_info['city']}, {weather_info['country']}")
            print(f"🌡 Temperature: {weather_info['temperature']}°C")
            print(f"🤔 Feels like: {weather_info['feels_like']}°C")
            print(f"💧 Humidity: {weather_info['humidity']}%")
            print(f"📊 Pressure: {weather_info['pressure']} hPa")
            print(f"💨 Wind: {weather_info['wind_speed']} m/s")
            print(f"🧭 Wind Direction: {weather_info['wind_direction']}°")
            print(f"☁ Condition: {weather_info['weather']}")
            print(f"👁 Visibility: {weather_info['visibility']} meters")
            print(f"☁ Cloudiness: {weather_info['cloudiness']}%")
            print(f"🌅 Sunrise: {weather_info['sunrise_time']}")
            print(f"🌇 Sunset: {weather_info['sunset_time']}")

            # Get weather icon
            icon_url = f"http://openweathermap.org/img/wn/{weather_info['icon']}@2x.png"
            print(f"Weather icon: {icon_url}")

            return weather_info
        else:
            print(f"Error: {data.get('message', 'Unknown error')}")
            return None

    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

# get_weather_by_coordinates("12.0322978", "75.7396422")