from www.scripts.open_meteo import get_daily_temps

test = get_daily_temps(39.0, -79.1, "2021-01-01", "2021-06-31") 

temps = test.copy()
# There are two different methods of calculating growing degree day
max = 29
min = 10
# This is method one
def gdd_method1(data, min, max, min_name = "min", max_name = "max", 
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
                min_name = "min",
                max_name = "max",
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

test2 = gdd_method1(temps, 10, 29, "temperature_2m_min", "temperature_2m_max")
test3 = gdd_method2(temps, 10, 29, "temperature_2m_min", "temperature_2m_max")

