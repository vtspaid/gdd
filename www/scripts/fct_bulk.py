import pandas as pd
import datetime
from www.scripts.open_meteo import get_daily_temps
import www.scripts.gdd_function as gdd_fun

def validate_table_columns(table):

    existing_columns = set(table.columns)
    required_columns_set = set(["site", "latitude", "longitude", "date"])
    
    missing_columns = required_columns_set - existing_columns
    
    if missing_columns:
        raise ValueError(f"Input table is missing required columns: {
            missing_columns}")
    
    print("Table columns validated successfully.")
    return None

# data_file2 = "www/test_data/test_sites.csv"
# data_file = "www/test_data/firefly_test.csv"
# datapath = data_file

def get_gdd_from_csv(filepath):
        data = pd.read_csv(filepath)
        data.columns = [col.lower() for col in data.columns]

        # Check that the required columns are present
        validate_table_columns(data)

        data['date'] = pd.to_datetime(data['date'], format = "mixed")

        data_fullsub = data[["site", "latitude", "longitude", "date"]].copy()
        data_fullsub = data_fullsub.drop_duplicates().reset_index()
        data_fullsub['year'] = data_fullsub['date'].dt.year
        output = list()
        for i in data_fullsub['year'].unique():
            data_sub = data_fullsub[data_fullsub['year'] == i]
            end_date = datetime.datetime.date(data_sub["date"].max())
            result = get_daily_temps(lat=list(data_sub["latitude"]), 
                                     long=list(data_sub["longitude"]),
                                     end=end_date, 
                                     sitenames=list(data_sub["site"]))
            result["date"] = result['date'].dt.tz_localize(None).dt.floor('D')
            result2 = gdd_fun.gdd_method1(result, 10, 29)
            output.append(result2)
        output_df = pd.concat(output)
        output_df.round(2)
        merged_df = pd.merge(data, output_df, 
        on=["site", "latitude", "longitude", "date"], how='left')
        return merged_df
