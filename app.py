from shiny import *
from shiny.types import FileInfo
import pandas as pd
import numpy as np
# from htmltools import HTML
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go

# utils:
from util import Get_sheet_names, data_prep, get_coordination, create_map, plot_map
# default map
loc = pd.read_excel('./data/flux_site_loc.xlsx')

app_ui = ui.page_fluid(
    ui.panel_title("View time series' for your site"),
    ui.layout_sidebar(
        ui.panel_sidebar(
            # ui.HTML(style = "height: 90vh; overflow-y: auto;"), 
            ui.input_checkbox_group("var", "Variable(s) to Visualize:", 
                {
                    "NEE" : "NEE",
                    "SW_IN" : "SW_IN",
                    "TA" : "TA",
                    "VPD" : "VPD",
                    "P" : "P",
                    "SWC" : "SWC",
                    "WS" : "WS",
                    "TS" : "TS",
                    "WTD" : "WTD",
                    "WTDdiff" : "WTDdiff",
                    "PDSI" : "PDSI",
                    "LAI_month_max" : "LAI_month_max",
                    "FAPAR_month_max" : "FAPAR_month_max",
                    "NDVI" : "NDVI",
                    "SIF_daily_8day" : "SIF_daily_8day",
                    "SIF_month" : "SIF_month"
                }),
                ui.output_ui("var_chosen"),
        ),
        ui.panel_main(
            ui.input_file(
                "file1", "Upload Your excel file here (.xlsx)", accept=[".xlsx"]
            ),
            ui.output_ui("path"),
            ui.output_plot("map", "Wetland Sites")
        )
    )
    
)

def server(input, output, session):
    @output
    @render.ui
    def var_chosen():
        req(input.var())
        return "You chose the variable(s) " + ", ".join(input.var())

    @output
    @render.ui
    def path():
        # create_map(df: pd.DataFrame)
        if input.file1() is None:
            return "Please upload a .xlsx file"
        f: list[FileInfo] = input.file1()
        df = pd.read_excel(f[0]["datapath"])
        return ui.HTML(df.to_html(classes="table table-striped"))
    
    # when a .xlsx file is uploaded, update the map output
    # gives error @render.plot doesn't know to render objects of type class str
    @output
    @render.plot
    def map():
        # create_map(df: pd.DataFrame)
        if input.file1() is None:
            return "Please upload a .xlsx file"
        f: list[FileInfo] = input.file1()
        loc = pd.read_excel(f[0]["datapath"])
        # # loc = pd.read_excel(f[0]["datapath"])
        # names = Get_sheet_names(input.file())
        # final_def = data_prep(f[0]["datapath"], names)
        map = plot_map(loc)
        return map

    # # when checkboxes change, update timeseries
    # @reactive.Effect
    # @reactive.event(input.var)
    # def _timeseries():
    #     variables = input.var()
    #     for variable in variables:
    #         make_timeseries(variable)

    # # function to make a timeseries plot given a variable to show
    # @reactive.Effect
    # def make_timeseries(variable: str):
    #     # do stuff to make it, this is a placholder
    #     np.random.seed(19680801)
    #     x_rand = 100 + 15 * np.random.randn(437)
    #     fig, ax = plt.subplots()
    #     ax.hist(x_rand, int(input.n()), density=True)
    #     ax.set_title(variable)
    #     # display plot
    #     ui.insert_ui(
    #         ui.output_plot("timeseries"),
    #         selector = "var",
    #         where = "afterEnd"
    #     )

app = App(app_ui, server)

