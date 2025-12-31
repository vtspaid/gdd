# Sidebar module
from shiny import Inputs, Outputs, Session, module, reactive,  ui

@module.ui
def sidebar_ui() -> ui.TagChild:
    return ui.sidebar(
        ui.row(
            ui.column(6, ui.input_numeric("lat", "Latitude", 0)),
            ui.column(6, ui.input_numeric("long", "Longitude", 0))
        ),
        ui.row(
            ui.column(6, ui.input_numeric("tbase", "Tbase", 10)),
            ui.column(6, ui.input_numeric("tmax", "Tmax", 50))
        ),
        ui.input_radio_buttons("unit", "Unit", ["Celsius", "Fahrenheit"], inline = True),
        ui.input_date("date", "Date"),
        ui.row(ui.column(6,
        ui.input_radio_buttons("method", "GDD Method", ["Method 1", "Method 2"]))),
        ui.input_action_button("get_gdd", "Get Growing Degree Days"),
         width = 370
    )
    

@module.server
def sidebar_server(input: Inputs, output: Outputs, session: Session, click):

    @reactive.Effect
    def _():
        val = click()
        if val:
            ui.update_numeric("lat", value=round(val[0], 9))
            ui.update_numeric("long", value=round(val[1], 9))


    return {
        'lat': reactive.calc(lambda: [input.lat()]),
        'long': reactive.calc(lambda: [input.long()]),
        'tbase': reactive.calc(lambda: input.tbase()),
        'tmax': reactive.calc(lambda: input.tmax()),
        'unit': reactive.calc(lambda: input.unit()),
        'date': reactive.calc(lambda: input.date()),
        'get_gdd': reactive.event(input.get_gdd), 
        'method': reactive.calc(lambda: input.method())
    }
