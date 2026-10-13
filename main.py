import requests


def get_coordinate(city):
    """Find the longitude and the latitude of the city"""
    r = requests.get(
        "https://geocoding-api.open-meteo.com/v1/search",
        params={"name": "Port Harcourt", "count": 1},
        timeout=7,
    )
    r.raise_for_status()

    print(r.json())


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
    


def display_weather_code(code):
    """Convert a weather condition to a readable format"""
    pass


def main():
    pass


if __name__ == "__main__":
    main()


print(get_coordinate("Lagos"))
print(get_coordinate("zzzzxq"))