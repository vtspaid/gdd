# Sidebar module
from shiny import Inputs, Outputs, Session, module, reactive,  ui

@module.ui
def sidebar_ui() -> ui.TagChild:
    return ui.sidebar(
        ui.row(
            ui.column(6, ui.input_numeric("lat", "Latitude", 10)),
            ui.column(6, ui.input_numeric("long", "Longitude", 0))
        ),
        ui.input_date("date", "Date"),
        ui.input_action_button("get_gdd", "Get Growing Degree Days"),
        ui.row(ui.column(6,
         ui.input_radio_buttons("method", "GDD Method", ["Method 1", "Method 2"])))
    )
    

@module.server
def sidebar_server(input: Inputs, output: Outputs, session: Session, click):

    @reactive.Effect
    def _():
        val = click()
        if val:
            ui.update_numeric("lat", value=val[0])
            ui.update_numeric("long", value=val[1])


    return {
        'lat': reactive.calc(lambda: [input.lat()]),
        'long': reactive.calc(lambda: [input.long()]),
        'date': reactive.calc(lambda: input.date()),
        'get_gdd': reactive.event(input.get_gdd), 
        'method': reactive.calc(lambda: input.method())
    }
