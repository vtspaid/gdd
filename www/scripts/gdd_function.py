from www.scripts.open_meteo import get_daily_temps

# This is method one
def gdd_method1(data, min, max, min_name = "temp_min", max_name = "temp_max", 
celsius = True):
    df = data.copy()
    if (not celsius):
        df.loc[:, [min_name, max_name]] = df.loc[:, [min_name, max_name]] * 9 / 5
        df.loc[:, [min_name, max_name]] = df.loc[:, [min_name, max_name]] + 32
    df["single_day_gd"] = ((df[max_name] + df[min_name]) / 2)
    df["single_day_gd"] = df["single_day_gd"].clip(lower=min, upper=max)
    df["single_day_gd"] = df["single_day_gd"] - min
    df["gdd"] = df["single_day_gd"].cumsum()
    return df

# This is method two
def gdd_method2(data,
                min,
                max,
                min_name = "temp_min",
                max_name = "temp_max",
                celsius = True
):
    df = data.copy()
    if (not celsius):
        df.loc[:, [min_name, max_name]] = df.loc[:, [min_name, max_name]] * 9 / 5
        df.loc[:, [min_name, max_name]] = df.loc[:, [min_name, max_name]] + 32
    df.loc[:, [min_name, max_name]] = df.loc[:, [min_name, max_name]].clip(
        lower=min,
        upper=max
    )
    df["single_day_gd"] = ((df[max_name] + df[min_name]) / 2) - min
    df["gdd"] = df["single_day_gd"].cumsum()
    return df

# mydate = "2021-06-30"
# test = datetime.datetime.date(mydate)
# mydate = datetime.datetime.strptime(mydate, "%Y-%m-%d")
# type(mydate)
# print(mydate)
# test = get_daily_temps(lat =39.0, long=-79.1, end=test) 
