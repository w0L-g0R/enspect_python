from settings import eev_indices
import inspect
import os
from typing import List

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import pandas as pd
import plotly.graph_objects as go
from dash import callback_context
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from gui.app import app
from gui.utils import show_callback_context
from dash import no_update

IDX = pd.IndexSlice


# def callback_on_reset_dropdowns(
#     idx_eev_1_value: str = no_update,
#     idx_eev_2_value: str = no_update,
#     idx_eev_3_value: str = no_update,
#     idx_eev_4_value: str = no_update,
#     idx_res_1_value: str = no_update,
#     idx_res_2_value: str = no_update,
# ):

#     return [
#         idx_eev_1_value,
#         idx_eev_2_value,
#         idx_eev_3_value,
#         idx_eev_4_value,
#         idx_res_1_value,
#         idx_res_2_value,
#     ]


def create_on_reset_dropdowns(graph_id: str):
    @app.callback(
        [

            Output(f"idx-eev-1-{graph_id}", "value"),
            Output(f"idx-eev-2-{graph_id}", "value"),
            Output(f"idx-eev-3-{graph_id}", "value"),
            Output(f"idx-eev-4-{graph_id}", "value"),
            Output(f"idx-res-0-{graph_id}", "value"),
            Output(f"idx-res-1-{graph_id}", "value"),
            Output(f"idx-res-2-{graph_id}", "value"),
        ],
        [
            Input(f"btn-setup-{graph_id}", "n_clicks"),
        ],
        [
            State(f"idx-eev-1-{graph_id}", "disabled"),
            State(f"idx-eev-2-{graph_id}", "disabled"),
            State(f"idx-eev-3-{graph_id}", "disabled"),
            State(f"idx-eev-4-{graph_id}", "disabled"),
            State(f"idx-res-0-{graph_id}", "disabled"),
            State(f"idx-res-1-{graph_id}", "disabled"),
            State(f"idx-res-2-{graph_id}", "disabled"),
        ]
    )
    def on_reset_dropdowns(
        n_clicks: List,
        *args
        # idx_1_options: List,
        # idx_2_options: List,
        # idx_3_options: List,
        # idx_4_options: List,
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
        print('states: ', states)
        inputs = ctx.inputs

        if triggered:

            # Store the selected dropdown item in a variable
            triggered_prop_id = triggered[0]["prop_id"]
            triggered_value = triggered[0]["value"]

            # if len(idx_1_options) == 1:
            #     print('idx: ', idx_1_options)
            idx_values = []
            print('args: ', args)

            for arg in args:
                if arg:
                    idx_values.append("Gesamt")
                else:
                    idx_values.append(no_update)

            return idx_values
            # return callback_on_reset_dropdowns()

        else:
            raise PreventUpdate
