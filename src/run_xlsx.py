import sys
import logging
from pathlib import Path
from pprint import pprint

from settings import file_paths, provinces
from data_structures.classes.dataset import DataSet
from logger.setup import setup_logging
from xlsx.utils import get_workbook, write_to_sheet

from xlsx.workbook import xlsx

# ////////////////////////////////////////////////////////////////////// INPUTS

setup_logging(
    console_log_actived=True,
    console_log_filter=None,
    console_out_level=logging.DEBUG,
)

aggregates = ["Bruttoinlandsverbrauch", "Importe"]
# aggregates = ["Bruttoinlandsverbrauch"]

energy_sources = [
    "Gesamtenergiebilanz",
    # "KOHLE",
    # "GAS",
]
years = list(range(2000, 2019, 1))

# wb_path = "tmp.xlsx"

# graphs = []
# wb = get_workbook(path=wb_path)

ds = DataSet(name=f"Set_1", file_paths=file_paths)

ds.add_stats_data_per_years(
    name="Bevölkerungsstatisik",
    file="pop", years=years, provinces=provinces,
)

ds.add_stats_data_per_years(
    name="Fahrleistung_PKW",
    file="km_pkw", years=years, provinces=provinces,
)

for aggregate in aggregates:

    logging.getLogger().error("/" * 80)
    logging.getLogger().error(f"Aggregate: {aggregate}")

    ds.add_eb_data_per_years(
        file="eev",
        energy_sources=energy_sources,
        aggregate=aggregate,
        years=years,
        provinces=provinces,
    )

    ds.add_eb_data_per_sector(
        file="sec",
        energy_sources=energy_sources,
        aggregate=aggregate,
        years=[2016, 2017],
        provinces=provinces,
        sectors=[
            "Produzierender Bereich",
            "Verkehr",
            "Öffentliche und Private Dienstleistungen",
            "Private Haushalte",
            "Landwirtschaft",
        ],
    )

    ds.add_indicator(

        aggregate=aggregate,

        numerator=[
            data for data in ds.objects.filter(
                name__contains=aggregate+"_Gesamtenergiebilanz", order="per_years")
        ],

        denominator=[
            data for data in ds.objects.filter(
                file="pop")
        ],

    )

ds.add_overlay(
    to_data=[
        data for data in ds.objects.filter(
            name__startswith="Bruttoinlandsverbrauch",
            order="per_years",
            is_KPI=False
        )
    ],
    overlays=[
        data for data in ds.objects.filter(
            file="km_pkw")
    ],
    scalings="absolute",
    chart_type="line",
)


g_data = [
    v for v in ds.objects.filter(
        # order="per_sector",
        aggregate__in=["Bruttoinlandsverbrauch", "Importe"],
        # is_KPI=False
    )
]


ov_data = [
    v.name for v in ds.objects.filter(
        # order="per_years",
        # aggregate__in=["Bruttoinlandsverbrauch", "Importe"],
        # is_KPI=False
        # has_overlay=True
    )
]

# print('ov_data: ', ov_data)
g_data_names = [x.name for x in g_data]
g_size = [sys.getsizeof(x) for x in g_data]

pprint(f'{g_data_names}')
pprint(f'{g_size}')


wb = xlsx(name="WB1", path="test.xlsx", sheets=aggregates)
try:
    wb.close()
except:
    pass

for data in g_data:

    if data.order == "per_sector":

        wb.write(data=data, sheet=data.aggregate, shares="over_columns")
    else:
        wb.write(data=data, sheet=data.aggregate,)


for sheet in wb.book.sheetnames:
    print('sheet: ', sheet)

    dimension = wb.book[sheet].calculate_dimension()
    wb.book[sheet].move_range(dimension, rows=0, cols=10)

    wb.style(ws=wb.book[sheet])

wb.book.save(wb.path)


wb.launch()

# print('wb: ', wb.worksheets)

# for data in kpi_data:
# print(data.frame)
# for ds in graphs:
#     ds.write_to_sheet(
#         scaled="absolute", aggregates=["Bruttoinlandsverbrauch"],
#     )


# print("ds: ", ds)

# pprint(sorted(g_data))

# kpi_data = [v for v in ds.objects.filter(is_KPI=True)]
