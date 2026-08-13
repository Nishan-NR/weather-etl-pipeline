import pandas as pd 
import json

with open('data/raw/weather_raw.json', 'r') as rf:
    data = json.load(rf)

print(type(data))

hourly_data = data["hourly"]

print(hourly_data.keys())

df = pd.DataFrame(hourly_data)
print(df.head())

# renaming the column head 
df = df.rename(columns={
    "time": "timestamp",
    "temperature_2m": "temperature",
    "relative_humidity_2m": "humidity",
    "wind_speed_10m": "wind_speed"
})

print("Shape:", df.shape)
print("\nColumns:")
print(df.columns)

print("\nMissing values:")
print(df.isnull().sum())

print("\nDuplicate rows:", df.duplicated().sum())

print(df.head())

df["timestamp"] = pd.to_datetime(df["timestamp"])
print(df.dtypes)

print("\nSummary statistics:")
print(df.describe())

print("\nInvalid humidity:", ((df["humidity"] < 0) | (df["humidity"] > 100)).sum())

print("Negative wind speeds:", (df["wind_speed"] < 0).sum())

df["latitude"] = data["latitude"]
df["longitude"] = data["longitude"]
df["timezone"] = data["timezone"]

df["city"] = "Kathmandu"

df.to_csv(
    "data/processed/weather_processed.csv",
    index=False
)


print(df.isnull().sum())
print(df.duplicated().sum())
print(df.describe())

df = df[
    [
        "timestamp",
        "city",
        "latitude",
        "longitude",
        "timezone",
        "temperature",
        "humidity",
        "wind_speed"
    ]
]

print(df.head())
print(df.dtypes)

output_path = "data/processed/weather_processed.csv"

df.to_csv(output_path, index=False)

print(f"Processed data saved to {output_path}")