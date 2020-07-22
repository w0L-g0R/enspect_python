import plotly.graph_objects as go
import json
import logging
import webbrowser
from pathlib import Path
from pprint import pformat
from typing import Type, TypeVar

import dash_bootstrap_components as dbc
import dash_html_components as html
from dash import callback_context
from dash.exceptions import PreventUpdate
from waitress import serve
from typing import List, Dict
from gui.app import app
import pickle
# from files.energiebilanzen.processing.eb_sheets import eb_sheets
# from settings import eb_indices
from pathlib import Path

# _____________________________________________________________________________
# /////////////////////////////////////////////////////////////////////// TYPES

dash_component = Type[TypeVar("component")]


def get_eb_indices():
    eb_indices_path = Path("src/files/energiebilanzen/pickles/indices.p")
    return pickle.load(open(eb_indices_path, "rb"))


def create_eev_energy_source_options(energy_sources: List):

    # energy_sources = list(reversed(energy_sources[69:])) + energy_sources[:69]
    energy_sources = energy_sources[::-1]

    return [{"label": x, "value": x} for enum, x in enumerate(energy_sources)]


def create_row_indices(_type: str):

    eb_indices = get_eb_indices()

    print('_type: ', _type)
    if _type == "EEV":
        indices = eb_indices["MIDX_EEV"]

    if _type == "Sektoren":
        indices = eb_indices["IDX_EEV_SECTORS"].iloc[2:]

    if _type == "Sektor Energie":
        indices = eb_indices["IDX_SECTOR_ENERGY"].iloc[2:]

    if _type == "ErnRL":
        indices = eb_indices["MIDX_RENEWABLES"].loc[:, :2]
        print('indices: ', indices)

    midx = []

    for enum, col in enumerate(indices.columns):
        _indices = list(indices[col].unique())
        _indices = [{"label": x, "value": x}
                    for enum, x in enumerate(_indices)]
        midx.append(_indices)

    return midx


def run_server(
    app: dash_component, connection: dict, development: bool = True, debug: bool = True
):

    if development:

        app.run_server(
            debug=True if debug else False,
            # dev_tools_props_check=False,
            # dev_tools_ui=False,
            dev_tools_hot_reload=True,
            port=connection["port"],
            host=connection["url"],
        )

    else:
        serve(app.server, host=connection["url"], port=connection["port"])

    return


# ___________________________________________________________________________
# /////////////////////////////////////////////////////////////////// BROWSER


def open_webbrowser(connection: dict, new: int):
    webbrowser.get().open(
        "".join(("http://", connection["url"], ":", connection["port"])),
        new=new,
        autoraise=True,
    )
    return


# _____________________________________________________________________________
# //////////////////////////////////////////////////////////// CALLBACK CONTEXT


def show_callback_context(func_name: str, file_name: str, verbose: bool = False):

    # Switch to debug in order to surpress console output
    logging.getLogger().debug(f"{func_name} @ {file_name}")
    logging.getLogger().warning(f"{func_name} @ {file_name}")

    ctx_msg = {
        "inputs": callback_context.inputs,
        "states": callback_context.states,
        "triggered": callback_context.triggered,
    }

    if verbose:
        logging.getLogger().debug("\n" + pformat(ctx_msg))


def get_layout_horizontal_bar_graphs(unit: str, title: str, height: int = 240):

    return go.Layout(
        title=dict(
            text=title,
            y=0.96,
            x=0,
            xanchor="left",
            yanchor="top",
            font_size=14,
            font_family="Quicksand",
        ),
        barmode="stack",
        hoverlabel=dict(bgcolor="white", font_size=14,),
        legend=dict(
            # yanchor='top',
            # xanchor='right',
            y=-0.15,
            x=0,
            # x=-.1,
            # y=-0.1,
            font=dict(family="Oswald, sans-serif",
                      size=14, color="whitesmoke"),
            bordercolor="whitesmoke",
            borderwidth=1,
        ),
        font=dict(family="Oswald Light, sans-serif",
                  size=14, color="lightblue"),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        # autosize=True,
        height=height,
        margin=dict(l=12, r=12, t=12, b=12, pad=24),
        showlegend=True,
        legend_orientation="h",
        template="plotly_dark",
        xaxis=dict(
            dtick=1,
            tickangle=35,
            showticklabels=True,
            # type: 'category',
            ticks="outside",
            tickcolor="black",
            ticklen=10,
            ticksuffix=" " + unit,
            showticksuffix="all",
            # domain=[0, 0.7]
            zeroline=True,
        ),
    )


def multiplicator(unit: str):

    if unit == "GWh":
        multiplicator = 0.27778

    if unit == "PJ":
        multiplicator = 0.001

    if unit == "TJ":
        multiplicator = 1

    return multiplicator
# def get_layout_with_datetime(unit: str, title: str, height: int = 360):

#     return go.Layout(
#         # title=dict(text=title, y=0.98, x=0.5,
#         #            xanchor="center", yanchor="top"),
#         # title=title,
#         barmode="stack",
#         # hoverlabel=dict(bgcolor="white", font_size=14,
#         #                 font_family="Quicksand"),
#         # legend=dict(
#         #     # yanchor='bottom',
#         #     # xanchor="center",
#         #     y=-0.18,
#         #     x=0.5,
#         #     # x=-.1,
#         #     # y=-0.1,
#         #     font=dict(family="Arial, sans-serif",
#         #               size=12, color="black"),
#         #     # bordercolor="whitesmoke",
#         #     # borderwidth=1,
#         # ),
#         # font=dict(family="Arial, sans-serif",
#         #           size=12, color="black"),
#         # paper_bgcolor="black",
#         # plot_bgcolor="black",
#         width=432,
#         # autosize=True,
#         height=440,
#         # margin=dict(l=48, r=48, t=24, b=0, pad=0),
#         # margin=dict(autoexpan),
#         showlegend=True,
#         legend_orientation="h",
#         template="plotly_white",
#         yaxis=dict(
#             ticks="outside",
#             # tickcolor="black",
#             ticklen=10,
#             # ticksuffix=" " + unit,
#             showticksuffix="all",
#             # domain=[0, 0.7]
#             zeroline=True,
#         ),
#         xaxis=dict(
#             # ticks="outside",
#             # tickcolor="black",
#             # ticklen=10,
#             # ticksuffix=" " + unit,
#             # showticksuffix="all",
#             # domain=[0, 0.7]
#             zeroline=True,
#             # zeroline_color="black",
#         ),
#     )


def get_graph_layout(unit: str, title: str):

    return go.Layout(
        title=dict(text=title, y=1, x=0.5,
                   xanchor="center", yanchor="top"),
        barmode="stack",
        showlegend=True,
        legend=dict(x=-0.1, y=-0.32),
        legend_orientation="h",
        template="plotly_white",
        margin=dict(l=0, r=0, t=60, b=0),
        width=496,
        height=400,
        yaxis_title=unit,

        xaxis=dict(
            dtick=1,
            tickangle=90,
            showticklabels=True,
            # type: 'category',
            # ticks="outside",
            # tickcolor="black",
            # ticklen=10,
            # ticksuffix=" " + unit,
            # showticksuffix="all",
            # domain=[0, 0.7]
            zeroline=True,
        ),
        yaxis=dict(
            ticks="outside",
            tickcolor="lightgrey",
            ticklen=5,
            # ticksuffix=" " + unit,
            # showticksuffix="all",
            # domain=[0, 0.7]
            zeroline=True,
        ),
    )
