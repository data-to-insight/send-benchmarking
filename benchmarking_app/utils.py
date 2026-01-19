import pandas as pd


def location_picker(row):
    if (row["country_name"] == "England") & (pd.isnull(row["region_name"])):
        return "England"
    elif (pd.notnull(row["region_name"])) & (pd.isnull(row["la_name"])):
        return row["region_name"]
    else:
        return row["la_name"]


# def chart_colour_picker(row, la_selected, region_selected):
#     if row['la_name'] == la_selected:
#         return la_selected
#     #elif (row['country_name'] == 'England') & (str(row['region_name']).strip() == ""):
#     elif (row['region_name'] == region_selected) & (pd.isnull(row['la_name'])):
#              return region_selected
#     elif (row['country_name'] == 'England') & (pd.isnull(row['region_name'])):
#         return 'England'
#     else:
#         return 'Other LAs'


def chart_colour_picker(row, la_selected, region_selected):
    if row == la_selected:
        return la_selected
    elif row == region_selected:
        return region_selected
    elif row == "England":
        return "England"
    else:
        return "Other LAs"
