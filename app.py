from www.scripts.open_meteo import get_daily_temps
from www.scripts.modules.sidebar_module import sidebar_ui, sidebar_server
from www.scripts.modules.map_module import map_ui, map_server
from www.scripts.fct_bulk import get_gdd_from_csv
import www.scripts.gdd_function as gdd_fun
from shiny import App, render, ui, reactive, req
import pandas as pd

pd.set_option('display.precision', 2)

# User interface (UI) definition
app_ui = ui.page_sidebar(

    # Sidebar
    sidebar_ui("sidebar"),

    ui.include_css("www/styles/custom.css"),

    map_ui("map"),

    ui.output_text("ans"),
    ui.tags.br(),
   
    ui.div(ui.p("Process Many Locations at Once"), class_="bulk_header"),
    ui.HTML("""To process many locations at once upload a CSV file containing
    The following columns 'Site', 'Latitude', 'Longitude' and 'Date'. Then
    hit the "Analyze CSV" button". A 
    csv containing the growing degree days for each unique row will be
    returned. All of the inputs from the sidebar are still used except the date,
     latitude and longitude.
    <br> <br>"""),
    ui.row(ui.column(4, ui.input_file("infile", "")),
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
        try:
            # Get the daily max and min for the time period
            temp_df = get_daily_temps(lat=get_reactive_values['lat'](),
                                    long=get_reactive_values['long'](),
                                    end=get_reactive_values['date']())

            # Determine if the units are in celsius or not
            if (get_reactive_values['unit']() == "Celsius"):
                celsius = True
            else:
                celsius = False

            # Run the calculations using either method 1 or 2
            if (get_reactive_values['method']() == "Method 1"):
                gdd_df = gdd_fun.gdd_method1(temp_df, 
                                            get_reactive_values['tbase'](),
                                            get_reactive_values['tmax'](),
                                            celsius = celsius)
            else:
                gdd_df = gdd_fun.gdd_method2(temp_df, 
                                            get_reactive_values['tbase'](),
                                            get_reactive_values['tmax'](),
                                            celsius = celsius)
            # Grab the last value of gdd in the returned dataframe
            gdd_result.set(f"GDD = {str(round(gdd_df["gdd"].iloc[-1], 2))}")
        except Exception as e:
            m = ui.modal(
                str(e),
                title="An error occurred. Please check inputs.",
                footer=ui.modal_button("Close"),
                easy_close=True,
            )
            ui.modal_show(m)
   
    # Display GDD
    @render.text
    def ans():
        return gdd_result.get()

    # Get GDD for multiple sites at once
    @reactive.Effect
    @reactive.event(input.run_bulk)
    def compute_bulk_gdd():
        try:
            req(input.infile)
            
            # Determine if the units are in celsius or not
            if (get_reactive_values['unit']() == "Celsius"):
                celsius = True
            else:
                celsius = False

            # Find the gdd for the csv
            bulk_data = get_gdd_from_csv(input.infile()[0]["datapath"],
            get_reactive_values['tbase'](),
            get_reactive_values['tmax'](),
            celsius,
            method = get_reactive_values['method']())

            # Set the output value
            bulk_result.set(bulk_data)
        except Exception as e:
            m = ui.modal(
                str(e),
                title="An error occurred. Please check inputs.",
                footer=ui.modal_button("Close"),
                easy_close=True,
            )
            ui.modal_show(m)

    # Display results of multiple sites at once
    @render.data_frame
    def bulk_output():
        result = bulk_result.get()
        if (not isinstance(result, str)):
            round_cols = ['gdd']
            for col in round_cols:
                result[col] = [f"{i:.{2}f}" for i in result[col]]
            result['latitude'] = [f"{i:.{6}f}" for i in result['latitude']]
            result['longitude'] = [f"{i:.{6}f}" for i in result['longitude']]
            result['date'] = [str(i.date()) for i in result['date']]
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
