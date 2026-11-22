# Sidebar module
from shiny import Inputs, Outputs, Session, module, reactive,  ui

@module.ui
def sidebar_ui(interactive=True) -> ui.TagChild:

    children = [
       ui.row(
           ui.column(6, ui.input_numeric("tbase", "Tbase", 10)),
           ui.column(6, ui.input_numeric("tmax", "Tmax", 50))
       ),
       ui.input_radio_buttons("unit", "Unit", ["Celsius", "Fahrenheit"], inline = True),
       ui.row(ui.column(6,
       ui.div(
           ui.input_radio_buttons("method", "GDD Method", ["Method 1", "Method 2"]))),
           title = "McMaster, G. S., & Wilhelm, W. W. (1997). Growing degree-days: one equation, two interpretations. Agricultural and forest meteorology, 87(4), 291-300."
       ),
       ui.div(
           ui.input_radio_buttons("source", "Data Source", ["openmetio", "daymet"]),
           title = "openmetio: https://open-meteo.com  daymet: https://daymet.ornl.gov/"
       )
    ]

    if interactive:
        children.append(
            ui.div(
                ui.input_date("date", "Date"),
                title = "Choose an end date to calculate gdd for"
            )
        )
    
    return ui.card(
        children
    )
    

@module.server
def sidebar_server(input: Inputs, output: Outputs, session: Session):

    return {
        'tbase': reactive.calc(lambda: input.tbase()),
        'tmax': reactive.calc(lambda: input.tmax()),
        'unit': reactive.calc(lambda: input.unit()),
        'date': reactive.calc(lambda: input.date()),
        'method': reactive.calc(lambda: input.method()),
        'source': reactive.calc(lambda: input.source())
    }
