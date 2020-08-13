import logging
import pickle
import pandas as pd

# from files.energiebilanzen.processing.eb_sheets import eb_sheets
from pathlib import Path
from pprint import pformat
from typing import List, Type, TypeVar

# _____________________________________________________________________________
# /////////////////////////////////////////////////////////////////////// TYPES


def multiplicator(unit: str, normalized: bool = False):
    print("unit: ", unit)

    if unit == "GWh":
        multiplicator = 0.27778

        if normalized:
            multiplicator = 1 / multiplicator * 100

    if unit == "TWh":
        multiplicator = 0.00027778

        if normalized:
            multiplicator = 1 / multiplicator * 100

    if unit == "PJ":
        multiplicator = 0.001

        if normalized:
            multiplicator = multiplicator * 1e8

    if unit in ["TJ", "MW", "h", "%"]:
        multiplicator = 1

        if normalized:
            multiplicator = multiplicator * 100
    return multiplicator


def create_eev_energy_source_options(energy_sources: List):

    # energy_sources = list(reversed(energy_sources[69:])) + energy_sources[:69]
    energy_sources = energy_sources[::-1]

    return [{"label": x, "value": x} for enum, x in enumerate(energy_sources)]


def create_row_indices(_type: str, eb_indices: pd.DataFrame):

    # eb_indices = get_eb_indices()

    if _type == "EEV":
        indices = eb_indices["MIDX_EEV"]

    if _type == "Sektoren":
        indices = eb_indices["IDX_EEV_SECTORS"].iloc[2:]

    if _type == "Sektor Energie":
        indices = eb_indices["IDX_SECTOR_ENERGY"].iloc[2:]

    if _type == "ErnRL":
        indices = eb_indices["MIDX_RENEWABLES"].loc[:, :2]

    midx = []

    for enum, col in enumerate(indices.columns):
        _indices = list(indices[col].unique())
        _indices = [{"label": x, "value": x}
                    for enum, x in enumerate(_indices)]
        midx.append(_indices)

    return midx
