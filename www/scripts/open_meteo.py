
import openmeteo_requests

import pandas as pd
import requests_cache
from retry_requests import retry

cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)

def get_daily_temps(lat, long, end, start=None, sitenames=None):


    if start is None:
        start = str(end.year) + "-01-01"
    print("did this even start")
    print("lat: ", lat, "; long: ", long, "start: ", start, "; end: ", end)
    # Make sure all required weather variables are listed here
    # The order of variables in hourly or daily is important to assign them correctly below
    url = "https://historical-forecast-api.open-meteo.com/v1/forecast"
    params = {
    	"latitude": lat,
    	"longitude": long,
    	"start_date": start,
    	"end_date": end,
    	"daily": ["temperature_2m_max", "temperature_2m_min"],
    	"timezone": "America/New_York",
    }
    responses = openmeteo.weather_api(url, params=params)

    # Initialize empty list to hold results
    dataframe_list = []

    if sitenames is None:
        sitenames = list(range(0, len(lat)))
        sitenames  = [i + 1 for i in sitenames]
    
    for i in range(len(lat)):
        # Process first location. Add a for-loop for multiple locations or weather models
        response = responses[i]

        # Process daily data. The order of variables needs to be the same as requested.
        daily = response.Daily()
        daily_temperature_2m_max = daily.Variables(0).ValuesAsNumpy()
        daily_temperature_2m_min = daily.Variables(1).ValuesAsNumpy()
        
        daily_data = {"date": pd.date_range(
        	start = pd.to_datetime(daily.Time(), unit = "s", utc = True),
        	end =  pd.to_datetime(daily.TimeEnd(), unit = "s", utc = True),
        	freq = pd.Timedelta(seconds = daily.Interval()),
        	inclusive = "left"
        )}
        daily_data["temp_max"] = daily_temperature_2m_max
        daily_data["temp_min"] = daily_temperature_2m_min
        daily_dataframe = pd.DataFrame(data = daily_data)
        daily_dataframe["latitude"] = lat[i]
        daily_dataframe["longitude"] = long[i]
        daily_dataframe["site"] = sitenames[i]

        dataframe_list.append(daily_dataframe)
    full_data = pd.concat(dataframe_list, ignore_index=True)
    print("data retrieved")
    return full_data
   