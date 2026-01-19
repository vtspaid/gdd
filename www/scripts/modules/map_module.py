# Map module

from shiny import Inputs, Outputs, Session, module, reactive, ui
import shinywidgets
from ipyleaflet import Map, basemaps

@module.ui
def map_ui() -> ui.TagChild:
    return ("Click on the Map to Select a Location. The Answer will appear below the map.",
        shinywidgets.output_widget("usa_map")
    )

@module.server
def map_server(input: Inputs, output: Outputs, session: Session):

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

    return click_location