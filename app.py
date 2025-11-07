from www.scripts.open_meteo import get_daily_temps
from www.scripts.gdd_function import gdd_method1
from shiny import App, render, ui, reactive

# User interface (UI) definition
app_ui = ui.page_sidebar(

    # Sidebar
    ui.sidebar(
        ui.row(
            ui.column(6, ui.input_numeric("lat", "Latitude", 0)),
            ui.column(6, ui.input_numeric("long", "Longitude", 0))
        ),
        ui.input_date("date", "Date"),
        ui.input_action_button("get_gdd", "Get Growing Degree Days")
    ),
    # A container for plot output
    ui.output_text("ans"),
    # A select input for choosing the variable to plot
    title = "Growing Degree Days Calculator"
)


# Server function provides access to client-side input values
def server(input):
    
    gdd_result = reactive.Value("")

    @reactive.effect
    @reactive.event(input.get_gdd)
    def compute_gdd():
        temp_df = get_daily_temps(lat=input.lat(), long=input.long(), end=input.date())
        gdd_df = gdd_method1(temp_df, 10, 29, "temperature_2m_min", "temperature_2m_max")
        gdd_result.set(f"GDD = {str(gdd_df["gdd"].iloc[-1])}")
   
    @render.text
    def ans():
        return gdd_result.get()

app = App(app_ui, server)

if __name__ == "__main__":
    app.run()
