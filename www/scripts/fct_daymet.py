import pydaymet as daymet
import pandas as pd


def get_daymet_temps(lat, long, end, start=None, sitenames=None):

    if sitenames is None:
        sitenames = list(range(0, len(lat)))
        sitenames  = [i + 1 for i in sitenames]

    in_coords = list()
    for i in range(0, len(lat)):
        in_coords.append((long[i], lat[i]))

# Retrieve daily data for precipitation and maximum temperature
# The data is returned as an xarray Dataset by default
    daily_data = daymet.get_bycoords(
        coords = in_coords,
        dates = [end.year],
        coords_id=sitenames,
        variables=["tmin", "tmax"],
        to_xarray=True
    )

    dates = pd.date_range(start=f"{end.year}-01-01", end=f"{end.year}-12-31")
    df_list = list()
    for i in range(0, len(lat)):
        data = daily_data.sel(id=sitenames[i]).to_dataframe()
        data['latitude'] = lat[i]
        data['longitude'] = long[i]
        data['date'] = pd.to_datetime(daily_data.time.values)

        df_list.append(data)

    result_df = pd.concat(df_list, ignore_index=True)
    result_df.rename(columns={
        'tmax': 'temp_max', 'tmin': 'temp_min', 'id' : 'site'
        }, inplace=True)

    result_df = result_df[result_df['date'] < str(end)]

    return result_df
