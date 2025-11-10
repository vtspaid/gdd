from www.scripts.open_meteo import get_daily_temps
from www.scripts.modules.sidebar_module import sidebar_ui, sidebar_server
from www.scripts.modules.map_module import map_ui, map_server
import www.scripts.gdd_function as gdd_fun
from shiny import App, render, ui, reactive, req
import datetime
import pandas as pd


# User interface (UI) definition
app_ui = ui.page_sidebar(

    # Sidebar
    sidebar_ui("sidebar"),
    map_ui("map"),
    ui.output_text("ans"),
    ui.row(ui.column(4, ui.input_file("infile", "Select for Bulk Analysis")),
           ui.column(4, ui.input_action_button("run_bulk", "Analyze CSV")),
           ui.column(4, ui.download_button("dl_data", "Download Results"))),
    ui.output_data_frame("bulk_output"),
    # A select input for choosing the variable to plot
    title = "Growing Degree Days Calculator"
)


# Server function provides access to client-side input values
def server(input, output, session):

    gdd_result = reactive.Value("")
    bulk_result = reactive.Value("")

    # Display the map and return lat and long in the click object
    click = map_server("map")

    # Return sidebar inputs, update lat and long with click
    get_reactive_values = sidebar_server("sidebar", click=click)

    # Return GDD based on sidebar inputs
    @reactive.Effect
    @get_reactive_values['get_gdd']
    def compute_gdd():
        temp_df = get_daily_temps(lat=get_reactive_values['lat'](),
                                  long=get_reactive_values['long'](),
                                  end=get_reactive_values['date']())
        if (get_reactive_values['method']() == "Method 1"):
            gdd_df = gdd_fun.gdd_method1(temp_df, 10, 29)
        else:
            gdd_df = gdd_fun.gdd_method2(temp_df, 10, 29)
        gdd_result.set(f"GDD = {str(gdd_df["gdd"].iloc[-1])}")
   
    # Display GDD
    @render.text
    def ans():
        return gdd_result.get()

    # Get GDD for multipl sites at once
    @reactive.Effect
    @reactive.event(input.run_bulk)
    def compute_bulk_gdd():
        req(input.infile)
        datapath = input.infile()[0]["datapath"]
        data = pd.read_csv(datapath)
        data.columns = [col.lower() for col in data.columns]
        data['date'] = pd.to_datetime(data['date'])
        data_sub = data[["site", "latitude", "longitude", "date"]].copy()
        data_sub = data_sub.drop_duplicates().reset_index()
        end_date = datetime.datetime.date(data_sub["date"].max())
        result = get_daily_temps(lat=data_sub["latitude"], 
                                long=data_sub["longitude"],
                                end=end_date, sitenames=data_sub["site"])
        result["date"] = result['date'].dt.tz_localize(None).dt.floor('D')
        result2 = gdd_fun.gdd_method1(result, 10, 29)
        merged_df = pd.merge(data, result2, 
        on=["site", "latitude", "longitude", "date"], how='left')
        bulk_result.set(merged_df)

    # Display results of multiple sites at once
    @render.data_frame
    def bulk_output():
        result = bulk_result.get()
        if (not isinstance(result, str)):
            return render.DataTable(result, height = "400pt")
        else:
            return None

    # Download results of multiple sites at once
    @render.download(filename="result_gdd.csv")
    def dl_data():
        # Get the DataFrame
        print("trying to dl")
        result = bulk_result.get()
        # Convert DataFrame to CSV string
        yield result.to_csv(index=False)

app = App(app_ui, server)

if __name__ == "__main__":
    app.run()
