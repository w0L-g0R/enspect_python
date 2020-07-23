from pathlib import Path
from typing import Union, List, Dict
import pandas as pd
import pickle
import numpy as np
import time

from eb_sheets import eb_sheets
from create_indices import create_eev_col_midx, create_renewables_col_midx
from create_dfs import create_eb_storage_dfs, create_idx_check_dfs
from assign_table_data import (
    assign_eev_table,
    assign_renewables_table,
    assign_sectors_consumption_table,
    assign_sector_energy_consumption_table,
)

from fetch_from_excel import fetch_energy_sources

pd.set_option("display.max_columns", 10)  # or 1000
pd.set_option("display.max_rows", None)  # or 1000
pd.set_option("display.width", None)  # or 1000

IDX = pd.IndexSlice

# //////////////////////////////////////////////////////////// CONVERT_EB_TO_DF


def convert_eb_to_df(
    balances_directory_path: Union[str, Path],
    row_indices_file_path: Union[str, Path],
    eb_sheets: List,
    last_year: int,
):

    bundeslaender = [
        "AT",
        "Bgd",
        "Ktn",
        "Noe",
        "Ooe",
        "Sbg",
        "Stk",
        "Tir",
        "Vbg",
        "Wie",
    ]

    # ///////////////////////////////////////////////////////////// GET INDICES

    # _____________________________________________________________ ROW INDICES

    row_indices = pd.read_excel(
        io=str(row_indices_file_path), sheet_name=None, na_filter=False, header=None,
    )

    # _________________________________________________________ COL MULTI INDEX

    # Create a column muliindex with levels [Bundesland, Energieträger, Jahre]
    eev_col_midx = create_eev_col_midx(last_year=last_year, sheets=eb_sheets)

    # Create a column muliindex with levels [Bundesland, Jahre]
    renewables_col_midx = create_renewables_col_midx(last_year=last_year)

    # _____________________________________________________ EEV ROW MULTI INDEX

    # Create a row muliindex with 5 levels for the EEV data

    eev_row_midx = pd.MultiIndex.from_tuples(
        tuples=[tuple(x) for x in row_indices["MIDX_EEV"].values],
        names=["IDX_0", "IDX_1", "IDX_2", "IDX_3", "IDX_4"],
    )

    # _____________________________________________________ EEV ROW MULTI INDEX

    # Create a row muliindex with 5 levels for the renewable data

    renewables_row_midx = pd.MultiIndex.from_tuples(
        tuples=[tuple(x) for x in row_indices["MIDX_RENEWABLES"].loc[:, :3].values],
        names=["IDX_0", "IDX_1", "IDX_2", "IDX_3"],
    )

    # ////////////////////////////////////////////////////// CREATE STORAGE DFS

    (
        eev_df,
        renewables_df,
        sector_consumptions_df,
        sector_energy_consumption_df,
    ) = create_eb_storage_dfs(
        eev_col_midx=eev_col_midx,
        renewables_col_midx=renewables_col_midx,
        row_indices=row_indices,
    )

    # ////////////////////////////////////// COLLECT ENERGY BALANCES FILE PATHS

    # Array to store energy balance file paths as pathlib objects
    eb_file_paths = []

    for _path in balances_directory_path.glob("*.xlsx"):
        eb_file_paths.append(str(Path(_path)))

    for bundesland in bundeslaender:

        print(
            "//////////////////////////  {}  /////////////////////////".format(
                bundesland
            )
        )

        # /////////////////////////////////////////////////////////// FIND PATH
        try:
            # Find corresponding excel file for bundesland
            balances_file_path = list(filter(lambda x: bundesland in x, eb_file_paths))[
                0
            ]

        # CHECK 1: Xlxs file not found or not existing
        except Exception as e:
            raise e

        # ////////////////////////////////////////////////////////// FETCH DATA
        years_range_data = pd.Series(data=eev_df.columns.unique(level="YEAR")).astype(
            "object"
        )

        dfs, renewables_sheet = fetch_energy_sources(
            balances_file_path=balances_file_path,
            eb_sheets=eb_sheets,
            years_range_data=years_range_data,
        )

        # //////////////////////////////////////////////////////////// CHECK DF

        (
            eev_idx_check_df,
            renewables_idx_check_df,
            sector_consumptions_idx_check_df,
            sector_energy_consumption_idx_check_df,
        ) = create_idx_check_dfs(row_indices=row_indices)

        if bundesland != "AT":

            # ////////////////////////////////////////////////////// RENEWABLES
            assign_renewables_table(
                renewables_df=renewables_df,
                renewables_sheet=renewables_sheet,
                row_indices=row_indices,
                bundesland=bundesland,
                renewables_idx_check_df=renewables_idx_check_df,
                years_range_data=years_range_data,
            )

        # for energy_source in ["Steinkohle"]:
        for energy_source in dfs:
            print("\nenergy_source: ", energy_source)

            # ///////////////////////////////////////////////////////////// EEV
            assign_eev_table(
                eev_df=eev_df,
                dfs=dfs,
                row_indices=row_indices,
                bundesland=bundesland,
                energy_source=energy_source,
                eev_idx_check_df=eev_idx_check_df,
                years_range_data=years_range_data,
            )

            # ///////////////////////////////////////////// SECTORS CONSUMPTION
            assign_sectors_consumption_table(
                sector_consumptions_df=sector_consumptions_df,
                dfs=dfs,
                bundesland=bundesland,
                energy_source=energy_source,
                sector_consumptions_idx_check_df=sector_consumptions_idx_check_df,
                years_range_data=years_range_data,
            )

            # /////////////////////////////////////// SECTOR ENERGY CONSUMPTION
            assign_sector_energy_consumption_table(
                sector_energy_consumption_df=sector_energy_consumption_df,
                dfs=dfs,
                bundesland=bundesland,
                energy_source=energy_source,
                sector_energy_consumption_idx_check_df=sector_energy_consumption_idx_check_df,
                years_range_data=years_range_data,
            )

        # ////////////////////////////////////////////////////////////// CHECKS

        renewables_idx_check_df.to_excel(
            balances_directory_path.parent
            / "checks"
            / "_".join([bundesland, "renewables_idx_check_df.xlsx"])
        )

        eev_idx_check_df.to_excel(
            balances_directory_path.parent
            / Path("checks")
            / "_".join([bundesland, "eev_idx_check_df.xlsx"])
        )

        sector_consumptions_idx_check_df.to_excel(
            balances_directory_path.parent
            / "checks"
            / "_".join([bundesland, "sector_consumptions_idx_check_df.xlsx"])
        )

        sector_energy_consumption_idx_check_df.to_excel(
            balances_directory_path.parent
            / "checks"
            / "_".join([bundesland, "sector_energy_consumption_idx_check_df.xlsx"])
        )

    # //////////////////////////////////////////////////// ADD MIDX ROW INDICES

    eev_df.set_index(eev_row_midx, inplace=True)
    eev_df.sort_index(inplace=True, axis="columns")

    renewables_df.set_index(renewables_row_midx, inplace=True)
    renewables_df.sort_index(inplace=True, axis="columns")

    # ////////////////////////////////////////////////////////////////// PICKLE

    pickle.dump(
        eev_df, open(balances_directory_path.parent / Path("pickles/eev_df.p"), "wb")
    )

    pickle.dump(
        sector_consumptions_df,
        open(
            balances_directory_path.parent / Path("pickles/sector_consumptions_df.p"),
            "wb",
        ),
    )

    pickle.dump(
        sector_energy_consumption_df,
        open(
            balances_directory_path.parent
            / Path("pickles/sector_energy_consumption_df.p"),
            "wb",
        ),
    )

    pickle.dump(
        renewables_df,
        open(balances_directory_path.parent / Path("pickles/renewables_df.p"), "wb"),
    )

    return


# ////////////////////////////////////////////////////////////////////// INPUTS

balances_directory_path = Path(
    "D:/_WORK/AEA/Projekte/bilanzen_monitor/src/files/energiebilanzen/data"
)

row_indices_file_path = Path(
    "D:/_WORK/AEA/Projekte/bilanzen_monitor/src/files/energiebilanzen/index/row_indices_eb.xlsx"
)

start = time.time()
print("###########################################################################")
print("start: ", start)
convert_eb_to_df(
    balances_directory_path=balances_directory_path,
    eb_sheets=eb_sheets,
    row_indices_file_path=row_indices_file_path,
    last_year=2018,
)
end = time.time()
print("end: ", end)
print(end - start)