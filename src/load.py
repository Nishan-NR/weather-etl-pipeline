from sqlalchemy import create_engine, DateTime, text
import pandas as pd
import os
from dotenv import load_dotenv
from sqlalchemy.engine import URL

load_dotenv()
# load_dotenv(override=True)



username = os.getenv("DB_USERNAME")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
port = int(os.getenv("DB_PORT"))
database = os.getenv("DB_NAME")



# print("Username:", username)
# print("Host:", host)
# print("Port:", port)
# print("Database:", database)

connection_url = URL.create(
    drivername="mysql+pymysql",
    username=username,
    password=password,
    host=host,
    port=port,
    database=database
)
# connection_string = (
#     f"mysql+pymysql://{username}:{password}"
#     f"@{host}:{port}/{database}"
# )

# engine = create_engine(connection_string)

# print("Database connection created successfully.")

engine = create_engine(connection_url)

try:
    with engine.connect() as connection:
        print("Successfully connected to MySQL!")

except Exception as e:
    print(f"Database connection failed: {e}")


# Read processed weather data
df = pd.read_csv("data/processed/weather_processed.csv")

print(f"Loaded {len(df)} rows from CSV")
df["timestamp"] = pd.to_datetime(df["timestamp"])

# Load data into MySQL
# df.to_sql(
#     "weather",
#     con=engine,
#     if_exists="append",
#     index=False,
#     dtype={
#         "timestamp": DateTime()
#     }
# )

insert_query = text("""
    INSERT INTO weather (
        timestamp,
        city,
        latitude,
        longitude,
        timezone,
        temperature,
        humidity,
        wind_speed
    )
    VALUES (
        :timestamp,
        :city,
        :latitude,
        :longitude,
        :timezone,
        :temperature,
        :humidity,
        :wind_speed
    )
    ON DUPLICATE KEY UPDATE
        latitude = VALUES(latitude),
        longitude = VALUES(longitude),
        timezone = VALUES(timezone),
        temperature = VALUES(temperature),
        humidity = VALUES(humidity),
        wind_speed = VALUES(wind_speed)
""")

with engine.begin() as connection:

    records = df.to_dict(orient="records")

    connection.execute(insert_query, records)

print("Weather data loaded successfully!")