
import openmeteo_requests

import pandas as pd
import requests_cache
import datetime
from retry_requests import retry

cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)

def get_daily_temps(lat, long, end, start=None, sitenames=None):


    if start is None:
        start = str(end.year) + "-01-01"
    print("did this even start")
    print("lat: ", lat, "; long: ", long, "start: ", start, "; end: ", end)

    # We have to split the operation into two different api calls if the date
    # asked for goes past today (forecast data)
    c_date = datetime.date.today()
    
    if end < c_date:
        hist_end = end
    else:
        hist_end = c_date - datetime.timedelta(days=1)


    # Make sure all required weather variables are listed here
    # The order of variables in hourly or daily is important to assign them correctly below
    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
    	"latitude": lat,
    	"longitude": long,
    	"start_date": start,
    	"end_date": hist_end,
    	"daily": ["temperature_2m_max", "temperature_2m_min"],
    	"timezone": "America/New_York",
    }
    responses = openmeteo.weather_api(url, params=params)

    if end >= c_date:
        print("running next round")
        forecast_url = "https://historical-forecast-api.open-meteo.com/v1/forecast"
        params_forecast = {
            "latitude": lat,
            "longitude": long,
            "start_date": c_date,
            "end_date": end,
            "daily": ["temperature_2m_max", "temperature_2m_min"],
            "timezone": "America/New_York",
        }
        responses2 = openmeteo.weather_api(forecast_url, params=params_forecast)

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
        print(len(daily_dataframe))
        if end >= c_date:
            response2 = responses2[i]
                    # Process daily data. The order of variables needs to be the same as requested.
            daily2 = response2.Daily()
            daily_temperature_2m_max2 = daily2.Variables(0).ValuesAsNumpy()
            daily_temperature_2m_min2 = daily2.Variables(1).ValuesAsNumpy()
            
            daily_data2 = {"date": pd.date_range(
                start = pd.to_datetime(daily2.Time(), unit = "s", utc = True),
                end =  pd.to_datetime(daily2.TimeEnd(), unit = "s", utc = True),
                freq = pd.Timedelta(seconds = daily2.Interval()),
                inclusive = "left"
            )}

            daily_data2["temp_max"] = daily_temperature_2m_max2
            daily_data2["temp_min"] = daily_temperature_2m_min2
            daily_dataframe2 = pd.DataFrame(data = daily_data2)
            print(len(daily_dataframe2))
            daily_dataframe = pd.concat(
                [daily_dataframe, daily_dataframe2], axis=0, ignore_index=True
                )

        print(len(daily_dataframe))
        daily_dataframe["latitude"] = lat[i]
        daily_dataframe["longitude"] = long[i]
        daily_dataframe["site"] = sitenames[i]

        dataframe_list.append(daily_dataframe)
    full_data = pd.concat(dataframe_list, ignore_index=True)
    print("data retrieved")
    return full_data
   