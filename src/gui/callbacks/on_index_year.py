import pickle
import dash_html_components as html

import inspect
import os
from typing import List, Dict
from pathlib import Path
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import pandas as pd
from dash import callback_context
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from gui.utils import multiplicator
from gui.app import app
from gui.utils import show_callback_context
from dash import no_update
IDX = pd.IndexSlice

# def callback_on_plot(
#     graph: object
# ):

#     return [
#         idx_0,
#         idx_1,
#         idx_2,
#         idx_3,
#         idx_4,
#         idx_0_disabled,
#         idx_1_disabled,
#         idx_2_disabled,
#         idx_3_disabled,
#         idx_4_disabled,
#     ]


def create_on_index_year(graph_id: str):
    @app.callback(
        Output(f"{graph_id}-scale", "options"),

        [
            Input(f"{graph_id}-index-year", "value"),
        ],
        [State(f"active-years", "value"), ]
    )
    def on_index_year(
        index_year: str,
        active_years: List
        # state_idx_eev_0: bool,
        # state_idx_eev_1: bool,
        # state_idx_eev_2: bool,
        # state_idx_eev_3: bool,
        # state_idx_eev_4: bool,
    ):

        show_callback_context(
            verbose=True,
            func_name=inspect.stack()[0][3],
            file_name=inspect.stack()[0][1].rsplit(os.sep, 1)[-1].upper(),
        )
        # Get callback information to define the triggered input
        ctx = callback_context
        triggered = ctx.triggered
        states = ctx.states
        inputs = ctx.inputs

        if triggered:

            active_years = [1987 + int(x) for x in active_years]
            print('active_years: ', active_years)

            print('min(active_years): ', min(active_years))
            print('max(active_years):: ', max(active_years))
            print('int(index_year): ', int(index_year))

            if int(index_year) >= min(active_years) and int(index_year) <= max(active_years):

                return [
                    {"label": "Absolut", "value": 1, },
                    {"label": "Normalisiert", "value": 2, },
                    {"label": "Index Jahr", "value": 3, "disabled": False},
                ]
            else:

                return no_update
        else:
            raise PreventUpdate
