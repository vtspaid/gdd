from www.scripts.open_meteo import get_daily_temps
import www.scripts.gdd_function as gdd_fun
from shiny import App, render, ui, reactive, req
import shinywidgets
from ipyleaflet import Map, basemaps
import datetime
import pandas as pd


# User interface (UI) definition
app_ui = ui.page_sidebar(

    # Sidebar
    ui.sidebar(
        ui.row(
            ui.column(6, ui.input_numeric("lat", "Latitude", 0)),
            ui.column(6, ui.input_numeric("long", "Longitude", 0))
        ),
        ui.input_date("date", "Date"),
        ui.input_action_button("get_gdd", "Get Growing Degree Days"),
        ui.row(ui.column(6,
         ui.input_radio_buttons("method", "GDD Method", ["Method 1", "Method 2"])))
    ),
    # A container for plot output
    shinywidgets.output_widget("usa_map"),
    ui.output_text("ans"),
    ui.row(ui.column(6, ui.input_file("infile", "Select for Bulk Analysis")),
           ui.column(6, ui.input_action_button("run_bulk", "Analyze CSV"))),
    ui.output_table("bulk_output"),
    # A select input for choosing the variable to plot
    title = "Growing Degree Days Calculator"
)


# Server function provides access to client-side input values
def server(input):

    # Reactive value to store click location
    click_location = reactive.Value(None)


    gdd_result = reactive.Value("")
    bulk_result = reactive.Value("")
    click_location = reactive.Value(None)

    @shinywidgets.render_widget
    def usa_map():
            # Define click handler
        def handle_click(**kwargs):
            if kwargs.get('type') == 'click':
                latlon = kwargs.get('coordinates')
                print(latlon)
                click_location.set(latlon)
        # Create an ipyleaflet map centered on the approximate center of the contiguous USA
        m = Map(
            center=(39.8283, -98.5795),  # Latitude and Longitude for center of USA
            zoom=4,
            basemap=basemaps.OpenStreetMap.Mapnik  # Use OpenStreetMap tiles for street view
        )
        m.on_interaction(handle_click)
        return m

    @reactive.effect
    def fake_name():
        req(click_location.get())
        loc = click_location.get()
        ui.update_numeric("lat", value = loc[0])
        ui.update_numeric("long", value = loc[1])

    @reactive.Effect
    @reactive.event(input.get_gdd)
    def compute_gdd():
        temp_df = get_daily_temps(lat=[input.lat()], long=[input.long()], end=input.date())
        if (input.method() == "Method 1"):
            gdd_df = gdd_fun.gdd_method1(temp_df, 10, 29)
        else:
            gdd_df = gdd_fun.gdd_method2(temp_df, 10, 29)
        gdd_result.set(f"GDD = {str(gdd_df["gdd"].iloc[-1])}")
   
    @render.text
    def ans():
        return gdd_result.get()

    @reactive.Effect
    @reactive.event(input.run_bulk)
    def compute_bulk_gdd():
        req(input.infile)
        print(input.infile())
        datapath = input.infile()[0]["datapath"]
        print("datapath is")
        print(datapath)
        data = pd.read_csv(datapath)
        data.columns = [col.lower() for col in data.columns]
        print(data.columns)
        data['date'] = pd.to_datetime(data['date'])
        data_sub = data[["site", "latitude", "longitude", "date"]].copy()
        data_sub = data_sub.drop_duplicates().reset_index()
        end_date = datetime.datetime.date(data_sub["date"].max())
        print("did we get here")
        result = get_daily_temps(lat=data_sub["latitude"], 
                                long=data_sub["longitude"],
                                end=end_date, sitenames=data_sub["site"])
        result["date"] = result['date'].dt.tz_localize(None).dt.floor('D')
        print("how about here")
        result2 = gdd_fun.gdd_method1(result, 10, 29)
        merged_df = pd.merge(data, result2, 
        on=["site", "latitude", "longitude", "date"], how='left')
        bulk_result.set(merged_df)

    @render.table
    def bulk_output():
        print("trying")
        result = bulk_result.get()
        if (not isinstance(result, str)):
            return result
        else:
            return None

app = App(app_ui, server)

if __name__ == "__main__":
    app.run()
