
disclaimer_text = (
 "This data is being provided to meet the need for easy access ",
"to current temperature and growing degree day information. The data sources ",
"have not been reviewed by myself, and I make not claim on the accuracy of ",
"the provided data. This data should not be used for scientific papers ",
"or other publications. Use at your own risk"
)

compare_text = (
    "The openmetio data and daymet data can provide very different answers. ",
    "I caution against using this data in any emperical way, and instead ",
    "using it for comparison only with itself. For example, using it to find ",
    "the growing degree days of a specific location and date the previous ",
    "and checking to see if that location is on pace to achieve that same ",
    "growing degree day in the current year when using all the same input ",
    "parameters."
)

openmetio_text = (
    "This app uses weather data from openmetio.com. For historical data, which ",
    "includes data up until the previous day, it uses the historical weather ",
    "API (https://open-meteo.com/en/docs/historical-weather-api).",
    "For data from the current date until two weeks from the current date it ",
    "Uses the weather forecast API (https://open-meteo.com/en/docs).",
    "Two important notes: The timezone is always assumed to be eastern, and ",
    "the weather forecast (at least in WV) always seems to be a warmer ",
    "than the actual weather. In other words, if you were to use the forecast ",
    "API for historical dates as well (which I did at first), you end up with ",
    "much higher GDD values than using the historical API. Since the forecast ",
    "API is only used for up to two weeks of data, the effect is probably ",
    "small."
)

daymet_text = (
    "This app also uses daymet data from https://daymet.ornl.gov/. I have not ",
    "done a thorough analysis to see which data set is more accurate. ",
    "The daymet data tends to predict fewer growing degree days than ",
    "openmetio.",
    "I did one comparison between daymet, PRISM (https://prism.oregonstate.edu/), and openmetio in WV and ",
    "dayment consistently had the fewest GDD, followed by PRISM, followed by ",
    "openmetio, and daymet and PRISM were somewhat closer to each other than ",
    "PRISM was to openmetio PRISM data can not be easily download for specific ",
    "coordinates as far as I'm aware or it would be included in this app.",
    " The main drawback of daymet is that it releases data one year ",
    "at a time, meaning for example that 2025 data will all be released at ",
    "once sometime in 2026, and therefore you cannot get realtime GDD"
)