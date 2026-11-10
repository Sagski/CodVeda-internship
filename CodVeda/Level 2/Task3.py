# -- API INTEGRATION --
# Fetches live weather and cryptocurrency data from free public APIs.
# No API key needed for either.

import requests   # type: ignore # sends HTTP requests — same library used in the scraper


# ── HELPERS ───────────────────────────────────────────────────────────────────

def get_json(url, params=None):
    """
    Makes a GET request to a URL and returns the parsed JSON as a Python dict.
    Returns None if anything goes wrong, so callers don't have to worry about crashes.

    params = optional dict of query parameters, e.g. {"city": "Lagos", "units": "metric"}
    requests will automatically append them to the URL as ?city=Lagos&units=metric
    """
    try:
        response = requests.get(url, params=params, timeout=10)
        # timeout=10 — give up after 10 seconds if the server doesn't respond

        response.raise_for_status()
        # raise_for_status() checks the HTTP status code.
        # 200 = success (silent). 404 = not found, 401 = bad API key, 500 = server error.
        # Any of those non-200 codes raises an HTTPError automatically.

        return response.json()
        # .json() reads the response body (plain text) and converts it
        # into a Python dictionary or list. This is the parsed data you work with.

    except requests.exceptions.ConnectionError:
        print("Error: No internet connection.")
    except requests.exceptions.Timeout:
        print("Error: The request timed out. Try again.")
    except requests.exceptions.HTTPError as e:
        print(f"Error: Bad response from server — {e}")
    except requests.exceptions.RequestException as e:
        # Catch-all for any other requests-related error
        print(f"Error: Something went wrong — {e}")

    return None   # reached only if one of the except blocks above ran


# ── FEATURE 1: WEATHER ────────────────────────────────────────────────────────

def get_weather(city, lat, lon):
    """
    Fetches current weather from Open-Meteo (open-meteo.com).
    Requires latitude and longitude instead of a city name, since Open-Meteo
    is a raw weather data API (no geocoding built in).
    """
    url = "https://api.open-meteo.com/v1/forecast"

    # These are query parameters — they get added to the URL automatically by requests:
    # https://api.open-meteo.com/v1/forecast?latitude=6.52&longitude=3.38&...
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m,relative_humidity_2m,wind_speed_10m,precipitation",
        # "current" tells the API which fields we want right now (not a forecast).
        # Multiple fields are comma-separated in one string.
        "wind_speed_unit": "kmh",
        "timezone": "auto"   # auto-detects timezone from the coordinates
    }

    data = get_json(url, params)

    if data is None:
        return   # get_json already printed the error

    # The API wraps the current values in a nested dict called "current".
    # We extract it once to avoid typing data["current"] over and over.
    current = data["current"]

    # f-strings let us embed variables directly inside a string using {curly braces}.
    # :.1f means: format as a float with 1 decimal place.
    print(f"\n--- Weather in {city} ---")
    print(f"Temperature   : {current['temperature_2m']:.1f} °C")
    print(f"Humidity      : {current['relative_humidity_2m']}%")
    print(f"Wind speed    : {current['wind_speed_10m']:.1f} km/h")
    print(f"Precipitation : {current['precipitation']} mm")


# ── FEATURE 2: CRYPTO PRICES ──────────────────────────────────────────────────

def get_crypto(coins):
    """
    Fetches live cryptocurrency prices from CoinGecko (coingecko.com).
    coins = a list of coin IDs, e.g. ["bitcoin", "ethereum", "solana"]
    """
    url = "https://api.coingecko.com/api/v3/simple/price"

    params = {
        "ids": ",".join(coins),
        # ",".join(coins) turns ["bitcoin", "ethereum"] into "bitcoin,ethereum"
        # The API expects a comma-separated string, not a Python list.
        "vs_currencies": "usd",          # prices in US dollars
        "include_24hr_change": "true"    # also return the % change over last 24 hours
    }

    data = get_json(url, params)

    if data is None:
        return

    print("\n--- Crypto prices (USD) ---")

    for coin in coins:
        # data looks like: {"bitcoin": {"usd": 65000, "usd_24h_change": 2.3}, ...}
        if coin not in data:
            # The coin ID wasn't recognised by the API — skip it gracefully
            print(f"  {coin}: not found (check the coin ID)")
            continue   # move to the next coin in the loop

        info = data[coin]
        price  = info["usd"]
        change = info.get("usd_24h_change", 0)
        # .get("key", default) is safer than ["key"] — returns the default
        # instead of crashing with a KeyError if the key is missing.

        # Show a + or - sign in front of the 24h change
        sign = "+" if change >= 0 else ""

        # :>10,.2f means: right-align in 10 chars, use commas, 2 decimal places.
        # e.g. "65,432.10" — makes the prices line up neatly in the terminal.
        print(f"  {coin.capitalize():<12} ${price:>12,.2f}   ({sign}{change:.2f}% 24h)")


# ── MAIN ──────────────────────────────────────────────────────────────────────

def main():
    print("Fetching live data...\n")

    # Lagos coordinates
    get_weather("Lagos, Nigeria", lat=6.5244, lon=3.3792)

    get_crypto(["bitcoin", "ethereum", "solana", "binancecoin"])


if __name__ == "__main__":
    main()