
# This is method one
def gdd_method1(data, min, max, min_name = "temp_min", max_name = "temp_max", 
celsius = True):
    print("starting gdd_method 1")
    df = data.copy()
    if (not celsius):
        df.loc[:, [min_name, max_name]] = df.loc[:, [min_name, max_name]] * 9 / 5
        df.loc[:, [min_name, max_name]] = df.loc[:, [min_name, max_name]] + 32
    df["single_day_gd"] = ((df[max_name] + df[min_name]) / 2)
    df["single_day_gd"] = df["single_day_gd"].clip(lower=min, upper=max)
    df["single_day_gd"] = df["single_day_gd"] - min
    df["gdd"] = df.groupby("site")["single_day_gd"].cumsum()
    df[max_name] = round(df[max_name], 2)
    df[min_name] = round(df[min_name], 2)
    print("ending gdd_method 1")
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
    df["gdd"] = df.groupby("site")["single_day_gd"].cumsum()
    df[max_name] = round(df[max_name], 2)
    df[min_name] = round(df[min_name], 2)
    return df

# mydate = "2021-06-30"
# mydate = datetime.datetime.strptime(mydate, "%Y-%m-%d")
# test = datetime.datetime.date(mydate)
# type(mydate)
# print(mydate)
# test2 = get_daily_temps(lat =[39.0, 39.654, 40], long=[-79.1, -80, -80], end=test) 

# gdd_df = gdd_method1(data=test2, min=10, max=29)