import requests

# ---------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------
API_KEY = "3e54cac6b28374baff88a1a12561062d"
CITY = "Islamabad"  # You can change this to any city
UNITS = "metric"    # Options: 'metric' (Celsius), 'imperial' (Fahrenheit)

def fetch_weather_report(city_name):
    """
    Fetches real-time weather data from OpenWeatherMap API.
    """
    # Constructing the API Endpoint
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}&units={UNITS}"

    print(f"--- Weather Report for {city_name} ---")
    
    try:
        # Sending the GET request
        response = requests.get(url)
        
        # Raising an exception for 4xx or 5xx errors
        response.raise_for_status() 

        # Parsing JSON data
        data = response.json()
        
        # Extracting specific data points
        temp = data['main']['temp']
        humidity = data['main']['humidity']
        weather_desc = data['weather'][0]['description']
        wind_speed = data['wind']['speed']

        print(f"Status: Connection Successful!")
        print(f"Temperature: {temp}°C")
        print(f"Condition: {weather_desc.capitalize()}")
        print(f"Humidity: {humidity}%")
        print(f"Wind Speed: {wind_speed} m/s")

    except requests.exceptions.HTTPError as http_err:
        if response.status_code == 401:
            print("Error 401: Invalid API Key or Activation in progress.")
        elif response.status_code == 404:
            print(f"Error 404: City '{city_name}' not found. Please check spelling.")
        else:
            print(f"HTTP Error occurred: {http_err}")
            
    except Exception as err:
        print(f"An unexpected error occurred: {err}")

# ---------------------------------------------------------
# EXECUTION
# ---------------------------------------------------------
if __name__ == "__main__":
    fetch_weather_report(CITY)