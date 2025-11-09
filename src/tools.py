import requests
from pydantic import BaseModel, Field
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder

from countryinfo import CountryInfo

geolocator = Nominatim(user_agent="time_agent_app", timeout=5)
tf = TimezoneFinder()

class CityTime(BaseModel):
    """City time object with city name and time."""
    name: str = Field(description="City name against which time value is set")
    time: str = Field(description="Time of the city, e.g. '10:30 AM'")

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

def get_capital_name(country: str) -> str:
  """
  Tool to get the capital name of the input `country` 
  (with correct spelling).
  Args:
    country: valid country name string
  Returns:
    str capital name of the country
  """
  # Create a CountryInfo object
  countryName = CountryInfo(country)

  # Get the capital city
  capital = countryName.capital()

  # Print the capital
  if capital:
      return capital
  else:
      raise ValueError(
            f"Could not find capital information for '{country}'. "
            "Please check the spelling or try a different country name."
        )

