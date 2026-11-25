
disclaimer_text = (
 "This data is being provided to meet the need for easy access ",
"to current temperature and growing degree day information. The data sources ",
"have not been reviewed by myself, and I make no claim on the accuracy of ",
"the provided data. Use at your own risk."
)

compare_text = (
    """
    The openmetio data and daymet data can provide very different answers.
    Therefore the most informative way to use this data is in comparison to
    itself. For example, you could use it to find
    the growing degree days of a specific location and date the previous year
    and checking to see if that location is on pace to achieve that same
    growing degree day in the current year.
    """
)

openmetio_text = (
    "This app uses weather data from openmetio.com. For historical data, which ",
    "includes data up until the previous day, it uses the historical weather ",
    "API (https://open-meteo.com/en/docs/historical-weather-api). ",
    "For data from the current date until two weeks from the current date it ",
    "uses the weather forecast API (https://open-meteo.com/en/docs)."
)

daymet_text = (
    "This app also uses Daymet data from https://daymet.ornl.gov. I have not ",
    "done a thorough analysis to see which data set is more accurate. ",
    "The Daymet data tends to predict fewer growing degree days than ",
    "openmetio.",
    "I did one comparison between Daymet, PRISM (https://prism.oregonstate.edu), and openmetio in WV and ",
    "dayment consistently had the fewest GDD, followed by PRISM, followed by ",
    "openmetio, and Daymet and PRISM were somewhat closer to each other than ",
    "PRISM was to openmetio. PRISM data can not be easily download for specific ",
    "coordinates as far as I'm aware or it would be included in this app.",
    " The main drawback of Daymet is that it releases data one year ",
    "at a time, meaning for example that 2025 data will all be released at ",
    "once sometime in 2026, and therefore you cannot get realtime GDD."
)