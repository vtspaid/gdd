# Map module

from shiny import Inputs, Outputs, Session, module, reactive, ui
import shinywidgets
from ipyleaflet import Map, basemaps

@module.ui
def map_ui() -> ui.TagChild:
    return (
        ui.card(
            ui.card_header(
                "Click on the map to select a coordinate, or enter coordinates in the sidebar."
            ),
            shinywidgets.output_widget("usa_map"),
            ui.card_footer(
                ui.row(
                ui.column(4, ui.input_numeric("lat", "Latitude", 0)),
                ui.column(4, ui.input_numeric("long", "Longitude", 0)),
                ui.column(4, ui.input_action_button("show", "Get Growing Degree Days"))
            )
            )
        )
    )

@module.server
def map_server(input: Inputs, output: Outputs, session: Session):

    click_location = reactive.Value(None)

    @reactive.Effect
    def _():
        val = click_location.get()
        if val is not None:
            ui.update_numeric("lat", value=round(val[0], 9))
            ui.update_numeric("long", value=round(val[1], 9))

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

    return click_location