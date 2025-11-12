from countryinfo import CountryInfo


def get_capital_name(country: str) -> str:
  """Return the capital name for the provided country via CountryInfo."""
  capital_finder = CountryInfo(country)
  capital = capital_finder.capital()

  if capital:
      return capital

  raise ValueError(
      f"Could not find capital information for '{country}'. "
      "Please check the spelling or try a different country name."
  )
