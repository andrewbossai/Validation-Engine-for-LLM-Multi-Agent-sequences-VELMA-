import python_weather
import asyncio

async def get_temp(location):
    async with python_weather.Client(unit=python_weather.IMPERIAL) as client:
        weather = await client.get(location)
    return weather.temperature

async def get_hum(location):
    async with python_weather.Client(unit=python_weather.IMPERIAL) as client:
        weather = await client.get(location)
    return weather.humidity

async def get_precip(location):
    async with python_weather.Client(unit=python_weather.IMPERIAL) as client:
        weather = await client.get(location)
    return weather.precipitation

async def use_weather(location):
    async with python_weather.Client(unit=python_weather.IMPERIAL) as client:
        weather = await client.get(location)
        return f"\n{location} Weather Output: Temp {weather.temperature}, Humidity {weather.humidity}, Precipitation {weather.precipitation}"

# print(asyncio.run(use_weather("New York")))