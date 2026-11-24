# Sidebar module
from shiny import Inputs, Outputs, Session, module, reactive, ui

tupper = ui.HTML("T<sub>UPPER</sub>")
tbase = ui.HTML("T<sub>BASE</sub>")

@module.ui
def sidebar_ui(interactive=True) -> ui.TagChild:

    children = [
        ui.row(
            ui.column(4, ui.input_numeric("tbase", tbase, 10)),
            ui.column(4, ui.input_numeric("tmax", tupper, 30)),

            ui.column(4, 
            ui.div("Use " + tupper, class_="control-label"),
            ui.div(ui.input_checkbox("use_max", None), style_="display:flex; justify-content:center;")
            ),
        ),
        ui.input_radio_buttons("unit", None, ["Celsius", "Fahrenheit"], inline=True),
        ui.div(
            ui.input_radio_buttons(
                "method", "GDD Method", ["Method 1", "Method 2"], inline=True
            )
        ),
        ui.div(
            ui.input_radio_buttons(
                "source", "Data Source", ["openmetio", "Daymet"], inline=True
            ),
            title="openmetio: https://open-meteo.com  Daymet: https://daymet.ornl.gov/",
        ),
        ui.row(
            ui.p("Day of Year to Start Counting", class_="control-label"),
            ui.column(
                6,
                ui.input_select(
                    "month",
                    None,
                    [
                        "January",
                        "February",
                        "March",
                        "April",
                        "May",
                        "June",
                        "July",
                        "August",
                        "September",
                        "October",
                        "November",
                        "December",
                    ],
                ),
            ),
            ui.column(4, ui.input_select("day", None, list(range(1, 32)))),
        ),
    ]

    if interactive:
        children.append(
            ui.div(
                ui.input_date("date", "Date"),
                title="Choose an end date to calculate gdd for",
            )
        )

    return ui.card(children, class_="input_card")


@module.server
def sidebar_server(input: Inputs, output: Outputs, session: Session):

    return {
        "tbase": reactive.calc(lambda: input.tbase()),
        "tmax": reactive.calc(lambda: input.tmax()),
        "use_max": reactive.calc(lambda: input.use_max()),
        "unit": reactive.calc(lambda: input.unit()),
        "month": reactive.calc(lambda: input.month()),
        "day": reactive.calc(lambda: input.day()),
        "date": reactive.calc(lambda: input.date()),
        "method": reactive.calc(lambda: input.method()),
        "source": reactive.calc(lambda: input.source()),
    }
