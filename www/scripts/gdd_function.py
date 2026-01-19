
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
    df["gdd"] = df.groupby(["site", "latitude", "longitude"])["single_day_gd"].cumsum()
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
    df["gdd"] = df.groupby(["site", "latitude", "longitude"])["single_day_gd"].cumsum()
    df[max_name] = round(df[max_name], 2)
    df[min_name] = round(df[min_name], 2)
    return df

def get_gdd(data,
                min,
                max,
                min_name = "temp_min",
                max_name = "temp_max",
                celsius = True,
                method = 1
):

    assert method in [1, 2], "Options for method argument are 1 or 2"
    if not isinstance(method, int):
        raise TypeError("method should be an integer (either 1 or 2)")

    if method == 1:
        return gdd_method1(data, min, max, min_name, max_name, celsius)

    if method == 2:
        return gdd_method2(data, min, max, min_name, max_name, celsius)
