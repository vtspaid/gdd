from www.scripts.open_meteo import get_daily_temps
import www.scripts.gdd_function as gdd_fun
from shiny import App, render, ui, reactive, req
import shinywidgets
from ipyleaflet import Map, basemaps
from shinywidgets import output_widget, render_widget
import ipyleaflet


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
    # A select input for choosing the variable to plot
    title = "Growing Degree Days Calculator"
)


# Server function provides access to client-side input values
def server(input):

    # Reactive value to store click location
    click_location = reactive.Value(None)


    gdd_result = reactive.Value("")
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
    def _():
        print("is this even running")
        req(click_location.get())
        loc = click_location.get()
        ui.update_numeric("lat", value = loc[0])
        ui.update_numeric("long", value = loc[1])

    @reactive.Effect
    @reactive.event(input.get_gdd)
    def compute_gdd():
        temp_df = get_daily_temps(lat=input.lat(), long=input.long(), end=input.date())
        if (input.method() == "Method 1"):
            gdd_df = gdd_fun.gdd_method1(temp_df, 10, 29)
        else:
            gdd_df = gdd_fun.gdd_method2(temp_df, 10, 29)
        gdd_result.set(f"GDD = {str(gdd_df["gdd"].iloc[-1])}")
   
    @render.text
    def ans():
        return gdd_result.get()

app = App(app_ui, server)

if __name__ == "__main__":
    app.run()
