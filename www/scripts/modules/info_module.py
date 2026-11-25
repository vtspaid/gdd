from shiny import Inputs, Outputs, Session, module, reactive, ui
import www.scripts.util_global_resources as gr

tupper = ui.HTML("T<sub>UPPER</sub>")
tbase = ui.HTML("T<sub>BASE</sub>")


@module.ui
def info_ui() -> ui.TagChild:

    return (
    ui.row(
        ui.column(
            9,
            ui.card(
                ui.navset_card_underline(
                    ui.nav_panel(
                        "About",
                        ui.h4("About This App"),
                        ui.p("""
                        This app was built specifically to aid in planning for
                        surveys of adult fireflies in West Virginia. It has 
                        been made public to make it accessible to other 
                        researchers. While built with fireflies in mind, it
                        has been made with flexible inputs so that it can be 
                        adapted to other uses. Additionally it is released 
                        under an open source license and the source code is 
                        available for anyone to modify for any reason.
                        """),
                        ui.br(),
                        ui.markdown(
                            "**Source code:** [https://github.com/vtspaid/gdd](https://github.com/vtspaid/gdd)"
                            ),
                        ui.br(),
                        ui.markdown("**Contact:** Vincent Spaid at vtspaid@gmail.com"),
                        ui.br(),
                        ui.h4("Growing Degree Days"),
                        ui.p("""
                        For fireflies, the most common version of growing
                        degrees is the one used in Faust and Weston (2009).  
                        """),
                        ui.br(),
                        ui.p("""
                        To use the method Faust describes, use 50 degrees
                        Fahrenheit for 
                        """, tbase, ", do not use a ", tupper,
                         " and use 'Method 2'"),
                        ui.br(),
                        ui.p("""
                        For more information about growing degree days please
                        read the sources below. 
                        """),
                        ui.br(),
                        ui.h5("References"),
                        ui.tags.ol(
                            ui.tags.li("Faust, L. F., & Weston, P. A. (2009). Degree-day prediction of adult emergence of Photinus carolinus (Coleoptera: Lampyridae). Environmental Entomology, 38(5), 1505-1512."),
                            ui.tags.li("McMaster, G. S., & Wilhelm, W. W. (1997). Growing degree-days: one equation, two interpretations. Agricultural and forest meteorology, 87(4), 291-300. "),
                        ),
                        ui.p("")
                    ),
                    ui.nav_panel(
                        "Input Options",
                        ui.tags.ul(
                            ui.tags.li(
                                ui.tags.b(tbase, ": "),
                                """
                A minimum threshold below which zero growth occurs. This input
                is not optional and is always used.
                """,
                            ),
                            ui.tags.li(
                                ui.tags.b(tupper, ": "),
                                """
                A maximum threshold above which growth does not occur. This
                input is optional.
                """,
                            ),
                            ui.tags.li(
                                ui.tags.b("Use ", tupper, " checkbox: "),
                                """
                Controls wether or not the upper threshold is applied.
                """,
                            ),
                            ui.tags.li(
                                ui.tags.b("Celsius or Fahrenheit: "),
                                """
                Controls the temperature units of both
                the inputs and the output.
                """,
                            ),
                            ui.tags.li(
                                ui.tags.b("GDD Method: "),
                                """
                See McMaster and Wilhelm (1997) for a complete 
                discussion of method 1 vs method 2. Method 1 calculates the
                average before comparing to the lower (or upper) threshold. 
                Method 2 compares the maximum and minimum temperatures to the
                threshold before calculating the average. Method 2 results in
                higher growing degree days in colder parts of the year.
                """,
                            ),
                            ui.tags.li(
                                ui.tags.b("Data Source: "),
                                """
                There are two sources of temperature data. See
                the 'Sources' tab for details.
                """,
                            ),
                            ui.tags.li(
                                ui.tags.b("Day of Year to Start Counting: "),
                                """
                Some researchers prefer a modified
                growing degree day where the earliest months of the year are 
                not counted. To start accumulating growing degree days on March
                1st, change the month dropdown to 'March' and the day dropdown
                to '1'.
                """,
                            ),
                            ui.tags.li(
                                ui.tags.b("Date: "),
                                """
                The last day to include for temperature data. Defaults to
                the current day, but can be set to past days, or even up to two
                weeks in the future if using openmetio as a source.
                """,
                            ),
                        ),
                    ),
                    ui.nav_panel("Sources", 
                           ui.div(
            ui.h3("Disclaimer"),
            ui.p(gr.disclaimer_text),
            ui.br(),
            ui.p(gr.compare_text),
            class_="info_div",
        ),
        ui.br(),
        ui.div(
            ui.h3("Data Sources"),
            ui.p("openmetio:"),
            ui.p(gr.openmetio_text),
            ui.br(),
            ui.p("Daymet:"),
            ui.p(gr.daymet_text),
            class_="info_div",
        ),
                    ),
                    ui.nav_panel("LICENSE",
                    ui.div(
                        ui.p("Copyright 2026 Vincent Spaid"),
                        ui.p(
                    """ 
Permission is hereby granted, free of charge, to any person obtaining a copy of this 
software and associated documentation files (the “Software”), to deal in the Software 
without restriction, including without limitation the rights to use, copy, modify, 
merge, publish, distribute, sublicense, and/or sell copies of the Software, and to 
permit persons to whom the Software is furnished to do so, subject to the following 
conditions:
"""
                            ),
                            ui.br(),
                            ui.p("""
The above copyright notice and this permission notice shall be included in all copies 
or substantial portions of the Software.
"""
                            ),
                            ui.br(),
                            ui.p("""
THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, 
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A 
PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT 
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF 
CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE 
OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

                    """), class_="info_div")
                )
            ),
        ),
        ui.column(
            3,
        ),
    )
    ))
