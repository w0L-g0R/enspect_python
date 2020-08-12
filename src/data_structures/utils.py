
import pandas as pd
import numpy as np
from copy import deepcopy
from settings import conversion_multiplicators


def add_sums(df: pd.DataFrame):

    # Create provinces sum column and years sum row
    # print("df sums: ", df)
    df["Sum"] = df.iloc[:, :-1].sum(axis=1)
    # print("df sums col: ", df)
    df = df.T
    # print("df sums T: ", df)
    df["Sum"] = df.sum(axis=1)

    return df.T


def add_means(df: pd.DataFrame):

    # Create provinces sum column and years sum row
    # print("df sums: ", df)
    df["Mean"] = df.iloc[:, :-1].mean(axis=1)
    # print("df sums col: ", df)
    df = df.T
    # print("df sums T: ", df)
    df["Mean"] = df.mean(axis=1)

    return df.T


def get_shares(
    df: pd.DataFrame, years: bool = False, provinces: bool = False,
):

    # NOTE:
    # Percentage values years
    df_shares = deepcopy(df.iloc[:-1, :])

    if provinces:
        df_shares = df_shares.T

        provinces_sums_per_year = df_shares.iloc[:-
                                                 2, :].sum(axis=0).replace(0, np.nan)

        # print("provinces_sums_per_year: ", provinces_sums_per_year)
        AT_sums_per_year = df_shares.iloc[-2, :].replace(0, np.nan)

        # Province share over sum of provinces, per year
        df_shares.iloc[:-
                       2, :].replace(0, np.nan).divide(provinces_sums_per_year)

        # try:
        # Percentage sum over provinces per year (== 1)
        df_shares.iloc[-1, :].replace(0,
                                      np.nan).divide(provinces_sums_per_year)
        # except BaseException:
        #     pass

        # Sum of selected province as a share of "AT", per year
        df_shares.loc["AT", :] = provinces_sums_per_year.divide(
            AT_sums_per_year)

        # print("df_shares: ", df_shares)
        # Check if row values sum up to 1
        if "Sum" in df_shares.columns:
            for col in df_shares.columns:
                assert round(df_shares[col].iloc[:-2].sum(axis=0), 3) == round(
                    df_shares[col].loc["Sum"], 3
                ), f"PROVINCES SHARES '{col}': Percentage value sum {df_shares[col].iloc[:-2].sum(axis=0)} does not match sum {df_shares[col].loc['Sum']}!"

        if "Mean" in df_shares.columns:
            for col in df_shares.columns:
                assert round(df_shares[col].iloc[:-2].mean(axis=0), 3) == round(
                    df_shares[col].loc["Mean"], 3
                ), f"PROVINCES SHARES '{col}': Percentage value sum {df_shares[col].iloc[:-2].mean(axis=0)} does not match sum {df_shares[col].loc['Mean']}!"

        return df_shares.T

    elif years:

        df_shares = df_shares / df_shares.sum(axis=0)

        # Check if all necessary sum values are given
        if sum(df_shares.sum(axis=0)) == len(df_shares.columns):

            df_shares.loc["Sum", :] = df_shares.sum(axis=0).values

        if "Sum" in df_shares.columns:

            # Check if row values sum up to 1
            for col in df_shares.columns:

                assert round(df_shares[col].iloc[:-1].sum(axis=0), 3) == round(
                    df_shares[col].loc["Sum"], 3
                ), f"YEARS SHARES: {col}: Percentage value sum {df_shares[col].sum(axis=0)-1} does not match sum {df_shares[col].loc['Sum']}!"

        if "Mean" in df_shares.index:

            # Check if row values sum up to 1
            for col in df_shares.columns:

                assert round(df_shares[col].iloc[:-1].mean(axis=0), 3) == round(
                    df_shares[col].loc["Mean"], 3
                ), f"YEARS SHARES: {col}: Percentage value sum {df_shares[col].mean(axis=0)-1} does not match sum {df_shares[col].loc['Mean']}!"

        return df_shares


def apply_single_index(df: pd.DataFrame):
    # Process df with years on index and provinces on columns
    df = df.to_frame().T.reset_index(drop=True).T
    df = df.droplevel((1), axis=0)
    df = df.T.stack().droplevel((0), axis=0)
    df.index.name = ""

    # Put "AT" at the end
    if "AT" in df.columns:
        df = df.reindex(columns=list(df.columns[1:]) + ["AT"])

    return df


def convert(df: pd.DataFrame, conversion: str):

    # Transform data values to new unit scale
    df *= conversion_multiplicators[conversion]

    # Assign new unit
    unit = conversion.split("_")[-1]
    print('unit: ', unit)

    return df, unit
