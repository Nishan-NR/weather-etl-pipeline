import requests
import json

url = "https://api.open-meteo.com/v1/forecast"


params = {
    "latitude": 27.7017,
    "longitude": 85.3206,
    "timezone": "Asia/Kathmandu",
    "hourly": ["temperature_2m", "relative_humidity_2m", "wind_speed_10m"],
}
try:
    response = requests.get(
        url, params=params, timeout=10
    )  # timeout= Don't wait forever if the API isn't responding
    response.raise_for_status()  # if api return 200 everthing is ok if not Python raises an exception instead of blindly trying to process bad data.

except requests.exceptions.RequestException as e:
    print(f"API request failed: {e}")
    exit()
# print(response.status_code)
# print(response.text)
print("Status:", response.status_code)
print("Content-Type:", response.headers.get("Content-Type"))
# print("Response URL:", response.url)

data = response.json()
with open("data/raw/weather_raw.json", "w") as f:
    json.dump(data, f, indent=4)

print("Raw weather data saved successfully.")

print(type(data))
print(data.keys())
print(data["hourly"].keys())

print("Times:", data["hourly"]["time"][:5])
print("Temperature:", data["hourly"]["temperature_2m"][:5])
print("Humidity:", data["hourly"]["relative_humidity_2m"][:5])
print("Wind speed:", data["hourly"]["wind_speed_10m"][:5])

# cities = {
#     "Kathmandu": (27.7172, 85.3240),
#     "Pokhara": (28.2096, 83.9856),
#     "Lalitpur": (27.6588, 85.3247),
# }
