import os

import pytest


@pytest.mark.dependency()
def test_over_years(
    test_dataset,
    test_nea_workbook,
    test_provinces,
    test_nea_energy_sources,
    test_nea_usage_categories,
    test_nea_balance_aggregates,
    test_launch_xlsx,
    test_write_to_xlsx,
):

    years = list(range(2000, 2019))

    ds = test_dataset

    ds.add_nea_data(
        energy_sources=test_nea_energy_sources,
        balance_aggregates=test_nea_balance_aggregates,
        usage_categories=test_nea_usage_categories,
        years=years,
        provinces=test_provinces,
        # per_usage_category=True,
        # per_balance_aggregate=True,
        # per_energy_source=True,
        per_years=True,
    )

    data_objects = [_data for _data in ds.objects.filter(per_years=True,)]

    test_write_to_xlsx(
        wb=test_nea_workbook, data_objects=data_objects, sheet_name="YEARS",
    )


@pytest.mark.dependency(depends=["test_over_years"])
def test_launch(test_launch_xlsx, test_nea_workbook):

    test_launch_xlsx(wb=test_nea_workbook)