from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("europe-weather")

OPEN_METEO_BASE = "https://api.open-meteo.com/v1/forecast"
GEOCODING_API = "https://geocoding-api.open-meteo.com/v1/search"
HEADERS = {"User-Agent": "europe-weather-agent/1.0"}


async def make_request(url: str, params: dict[str, Any]) -> dict[str, Any] | None:
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, params=params, headers=HEADERS, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None


async def geocode_city(city: str) -> tuple[float, float] | None:
    data = await make_request(GEOCODING_API, {"name": city, "count": 1})
    if not data or "results" not in data or not data["results"]:
        return None
    lat = data["results"][0]["latitude"]
    lon = data["results"][0]["longitude"]
    return lat, lon


@mcp.tool()
async def get_forecast(city: str) -> str:
    """Get the 5-day weather forecast for a European city.

    Args:
        city: Name of a city (e.g. "Paris", "Berlin", "Madrid")
    """
    location = await geocode_city(city)
    if not location:
        return f"Could not find the city '{city}'. Please try another."

    lat, lon = location
    params = {
        "latitude": lat,
        "longitude": lon,
        "daily": "temperature_2m_max,temperature_2m_min,weathercode",
        "timezone": "auto",
    }

    data = await make_request(OPEN_METEO_BASE, params)
    if not data or "daily" not in data:
        return f"Could not fetch forecast for {city}."

    daily = data["daily"]
    dates = daily["time"]
    temps_max = daily["temperature_2m_max"]
    temps_min = daily["temperature_2m_min"]
    codes = daily["weathercode"]

    # Optionally, map weather codes to emojis or descriptions
    forecast_lines = []
    for i in range(min(5, len(dates))):
        forecast_lines.append(
            f"{dates[i]}:\n  High: {temps_max[i]}°C  Low: {temps_min[i]}°C  Code: {codes[i]}"
        )

    return "\n\n".join(forecast_lines)


if __name__ == "__main__":
    mcp.run(transport="stdio")