import requests
from typing import List
from pydantic import BaseModel, Field
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder

geolocator = Nominatim(user_agent="time_agent_app", timeout=5)
tf = TimezoneFinder()

class CityTime(BaseModel):
    """City time object with city name and time."""
    name: str = Field(description="City name against which time value is set")
    time: str = Field(description="Time of the city, e.g. '10:30 AM'")

class Timezone(BaseModel):
    """World standard Timezone from geocoding + TimezoneFinder."""
    place: str = Field(description="Original place text provided by the user")
    timezone: str = Field(
        description="IANA timezone identifier such as 'Asia/Karachi', 'Asia/Dubai', etc."
    )

def get_time_zone(place: str) -> Timezone:
    """
    Tool to determine the timezone of a city/area/country.
    """
    if not place:
        raise ValueError("The 'place' parameter must be a non-empty string.")

    location = geolocator.geocode(place, language="en", exactly_one=True)
    if not location:
        raise ValueError(f"Could not find location for place: {place}")

    lat = location.latitude
    lon = location.longitude

    # Debug info
    print("---Location---")
    print("Input place:", place)
    print("Resolved address:", location.address)
    print("Lat/Lon:", lat, lon)

    # 1) Main lookup
    tz = tf.timezone_at(lng=lon, lat=lat)

    # 2) Fallback near coasts / borders
    if tz is None:
        tz = tf.timezone_at_land(lng=lon, lat=lat)

    # 3) Optional: nearest zone as last resort
    # from timezonefinder import closest_timezone_at
    # if tz is None:
    #     tz = tf.closest_timezone_at(lng=lon, lat=lat)

    if tz is None:
        raise ValueError(
            f"Could not determine a timezone for '{place}' at ({lat}, {lon}). "
            "Ask the user for a more specific city (e.g. 'Islamabad, Pakistan')."
        )

    print("Timezone:", tz)
    return Timezone(place=place, timezone=tz)

def get_current_time(city: str, timezone: str) -> CityTime:
    """
    Tool to fetch the current time for the city using the given IANA timezone.

    `timezone` must be a valid string such as 'Asia/Karachi', 'Asia/Dubai', etc.
    """
    if not timezone:
        raise ValueError(
            "Parameter 'timezone' must be a non-empty IANA timezone string, "
            "for example 'Asia/Karachi' or 'Asia/Dubai'."
        )

    url = f"https://worldtimeapi.org/api/timezone/{timezone}"
    resp = requests.get(url, timeout=5)
    resp.raise_for_status()
    data = resp.json()

    # Example datetime: "2025-11-08T10:42:49.247759-06:00"
    datetime_iso = data["datetime"]
    # If you want "HH:MM" instead of full ISO, you can slice:
    # local_time = datetime_iso[11:16]
    # return CityTime(name=city, time=local_time)

    return CityTime(name=city, time=datetime_iso)