import requests


def get_coordinate(city):
    """Return (latitude, longitude, display_name) for a city, or None if not found or the request fails."""
    try:
        response = requests.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={"name": city, "count": 1},
            timeout=7,
        )
        response.raise_for_status()
        results = response.json().get("results")
    except requests.exceptions.RequestException:
        return None

    if not results:
        return None

    place = results[0]
    return place["latitude"], place["longitude"], f"{place['name']}, {place['country']}"


def get_weather(latitude, longitude):
    """Get the weather condition of the given coordinates"""
    try:
        response = requests.get(
                "https://api.open-meteo.com/v1/forecast",
                    params={
                        "latitude": latitude, 
                        "longitude": longitude, 
                        "current_weather": True
                        },
                    timeout=5
        )
        response.raise_for_status()
        data = response.json()
        return data["current_weather"]
    except (requests.exceptions.RequestException, KeyError):
        return None
    
weather_codes = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    56: "Light freezing drizzle",
    57: "Dense freezing drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    66: "Light freezing rain",
    67: "Heavy freezing rain",
    71: "Slight snowfall",
    73: "Moderate snowfall",
    75: "Heavy snowfall",
    77: "Snow grains",
    80: "Slight rain showers",
    81: "Moderate rain showers",
    82: "Violent rain showers",
    85: "Slight snow showers",
    86: "Heavy snow showers",
    95: "Thunderstorm",
    96: "Thunderstorm with slight hail",
    97: "Heavy thunderstorm",
    99: "Thunderstorm with heavy hail",
}

def display_weather_code(code):
    """Convert a weather condition to a readable format"""
    return weather_codes.get(code, "unknown")

def format_weather(name, weather):
    """Return a multi-line report string for a city and its weather dict."""
    temperature = weather["temperature"]
    wind = weather["windspeed"]
    conditions = display_weather_code(weather["weathercode"])

    return (
        f"{name}\n"
        f"Temperature: {temperature}°C\n"
        f"Wind: {wind} km/h\n"
        f"Conditions: {conditions}"
    )

def main():
    while True:
        city = input("Enter name of city, or Quit to quit: ").lower().strip()
        if city == "quit":
            break
        if not city:
            print("Enter a city name")
            continue
        result = get_coordinate(city)
        if result is None:
            print(f"{city} wasnt't  found")
            continue
        latitude, longitude, name = result

        weather = get_weather(latitude, longitude)
        if weather is None:
                print("Couldn't fetch the weather right now.")
                continue
        print(name)
        print(weather) 

if __name__ == "__main__":
    main()

