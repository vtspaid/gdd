# Sidebar module
from shiny import Inputs, Outputs, Session, module, reactive, ui


@module.ui
def sidebar_ui(interactive=True) -> ui.TagChild:

    children = [
        ui.row(
            ui.column(6, ui.input_numeric("tbase", "Tbase", 10)),
            ui.column(6, ui.input_numeric("tmax", "Tmax", 50)),
        ),
        ui.input_radio_buttons("unit", None, ["Celsius", "Fahrenheit"], inline=True),
        ui.div(
            ui.input_radio_buttons(
                "method", "GDD Method", ["Method 1", "Method 2"], inline=True
            )
        ),
        ui.div(
            ui.input_radio_buttons(
                "source", "Data Source", ["openmetio", "daymet"], inline=True
            ),
            title="openmetio: https://open-meteo.com  daymet: https://daymet.ornl.gov/",
        ),
        ui.row(
            ui.p("Day of Year to Start Counting", class_="control-label"),
            ui.column(
                6,
                ui.input_select(
                    "start_month",
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
            ui.column(4, ui.input_select("start_day", None, list(range(1, 32)))),
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
        "unit": reactive.calc(lambda: input.unit()),
        "date": reactive.calc(lambda: input.date()),
        "method": reactive.calc(lambda: input.method()),
        "source": reactive.calc(lambda: input.source()),
    }
