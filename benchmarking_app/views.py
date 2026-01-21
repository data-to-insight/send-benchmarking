import pandas as pd
import plotly.express as px
from glob import glob
import os

from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse

from send_benchmarking.settings import BASE_DIR
from benchmarking_app.forms import (
    SingleYearChoice,
    TrendChoice,
    SingleYearChoiceEHCP,
    SelectEHCPDataset,
)

from benchmarking_app.utils import chart_colour_picker, location_picker


def home(request):
    text = "hello"
    return render(
        request,
        "benchmarking_app/views/home.html",
    )


def select_ehcp_dataset(request):
    files = glob(os.path.join(BASE_DIR, "static/EHCP Data/*.csv"))

    dfs = {}

    for file in files:
        with open(file) as f:
            name = file.split(sep="/")[-1][:-4]
            dfs[name] = pd.read_csv(file)

    datasets = {dataset: dataset for dataset in list(dfs.keys())}

    form = SelectEHCPDataset(
        request.POST or None,
        dataset_choices=datasets,
        initial={
            "dataset": "requests",
        },
    )
    if form.is_valid():
        dataset_selected = form["dataset"].value()
        request.session["dataset_selected"] = dataset_selected
        return HttpResponseRedirect(reverse("single_year_ehcp_graphs"))
    return render(
        request, "benchmarking_app/views/select_ehcp_dataset.html", {"form": form}
    )


def single_year_ehcp_graphs(request):
    if "dataset_selected" in request.session:
        dataset_selected = request.session["dataset_selected"]
    else:
        dataset_selected = "requests"

    filepath = os.path.join(BASE_DIR, "static/EHCP Data/", f"{dataset_selected}.csv")
    with open(filepath) as f:
        df = pd.read_csv(f)

    with open(BASE_DIR / "static/SEND_data/stat neighbours.csv") as f:
        stat_neighbours = pd.read_csv(f)

    measures = df.columns[12:]

    form = SingleYearChoiceEHCP(
        request.POST or None,
        year_choices={year: year for year in df["time_period"].unique()},
        la_choices={la: la for la in df[df["la_name"].notna()]["la_name"].unique()},
        breakdown_topic_choices={
            topic: topic for topic in df["breakdown_topic"].unique()
        },
        breakdown_choices={
            breakdown: breakdown for breakdown in df["breakdown"].unique()
        },
        measure_choices={measure: measure for measure in measures},
        initial={
            "breakdown_topic": list(df["breakdown_topic"].unique())[0],
            "breakdown": list(df["breakdown"].unique())[0],
            "measure": measures[0],
        },
    )
    if form.is_valid():
        la_selected = form["la"].value()
        year = str(form["year"].value())
        breakdown_topic_selected = form["breakdown_topic"].value()
        breakdown_selected = form["breakdown"].value()
        measure_selected = form["measure"].value()
    else:
        la_selected = "Gateshead"
        year = "2024"
        breakdown_topic_selected = list(df["breakdown_topic"].unique())[0]
        breakdown_selected = list(df["breakdown"].unique())[0]
        measure_selected = measures[0]

    region_selected = df[df["la_name"] == la_selected]["region_name"].to_list()[0]

    if measure_selected[-2:] == "pc":
        df = df[
            (df["time_period"].astype("str") == str(year))
            & (df["breakdown_topic"] == breakdown_topic_selected)
            & (df["breakdown"] == breakdown_selected)
        ].copy()
    else:
        df = df[
            (df["time_period"].astype("str") == str(year))
            & (df["breakdown_topic"] == breakdown_topic_selected)
            & (df["breakdown"] == breakdown_selected)
            & (df["la_name"].notna())
        ].copy()

    df[measure_selected] = pd.to_numeric(df[measure_selected], errors="coerce")

    df["location_name"] = df.apply(location_picker, axis=1)

    

    stat_neighbours_list = stat_neighbours[la_selected].to_list()

    # We need a location name column for the chart, otherwise la_name values htat are empty (eg the whole of england or a region) don't show up
    df["chart_colour"] = df["location_name"].apply(
        chart_colour_picker,
        la_selected=la_selected,
        region_selected=region_selected,
        stat_neighbours_list=stat_neighbours_list,
    )

    plot = px.bar(
        df,
        y="location_name",
        x=measure_selected,
        title=measure_selected,
        labels={
            "location_name": "LA",
        },
        color="chart_colour",
    )

    plot.update_layout(
        xaxis={
            "categoryorder": "total descending",
        },
        height=1000,
    )
    plot.update_yaxes(showticklabels=False)

    plot = plot.to_html()

    text = request.session["dataset_selected"]

    return render(
        request,
        "benchmarking_app/views/single_year_ehcp_graphs.html",
        {"text": text, "plot": plot, "form": form},
    )


def single_year_graphs(request):

    with open(BASE_DIR / "static/SEND_data/sen_phase_type_.csv") as f:
        phase_type = pd.read_csv(f)
    with open(BASE_DIR / "static/SEND_data/stat neighbours.csv") as f:
        stat_neighbours = pd.read_csv(f)

    # data manipulation
    phase_type["ehc_plan_percent_float"] = pd.to_numeric(
        phase_type["ehc_plan_percent"], errors="coerce"
    )

    form = SingleYearChoice(
        request.POST or None,
        year_choices={year: year for year in phase_type["time_period"].unique()},
        la_choices={
            la: la
            for la in phase_type[phase_type["la_name"].notna()]["la_name"].unique()
        },
        phase_choices={
            phase: phase for phase in phase_type["phase_type_grouping"].unique()
        },
        establishment_choices={
            establishment: establishment
            for establishment in phase_type["type_of_establishment"].unique()
        },
        initial={"phase": "Total", "establishment": "Total"},
    )
    if form.is_valid():
        la_selected = form["la"].value()
        year = str(form["year"].value())
        phase_selected = form["phase"].value()
        establishment = form["establishment"].value()
        establishment = [establishment for establishment in establishment]
    else:
        la_selected = "Rochdale"
        year = "202425"
        phase_selected = "Total"
        establishment = ["Total"]

    phase_slice = phase_type[
        (phase_type["phase_type_grouping"] == phase_selected)
        & (phase_type["type_of_establishment"].isin(establishment))
        & (phase_type["time_period"].astype("str") == year)
        & (phase_type["hospital_school"] == "Total")
    ]

    phase_slice["location_name"] = phase_slice.apply(location_picker, axis=1)

    region_selected = phase_slice[phase_slice["la_name"] == la_selected][
        "region_name"
    ].to_list()[0]

    stat_neighbours_list = stat_neighbours[la_selected].to_list()

    # We need a location name column for the chart, otherwise la_name values htat are empty (eg the whole of england or a region) don't show up
    phase_slice["chart_colour"] = phase_slice["location_name"].apply(
        chart_colour_picker,
        la_selected=la_selected,
        region_selected=region_selected,
        stat_neighbours_list=stat_neighbours_list,
    )

    plot = px.bar(
        phase_slice,
        y="location_name",
        x="ehc_plan_percent_float",
        color="chart_colour",
        title="Percent of CYP with EHC Plan",
        labels={
            "location_name": "LA",
            "ehc_plan_percent_float": "Percent of CYP with EHC plan",
            "chart_colour": "",
        },
    )

    plot.update_layout(
        yaxis={
            "categoryorder": "total descending",
        },
        height=1000,
    )
    plot.update_yaxes(showticklabels=False)

    plot = plot.to_html()

    return render(
        request,
        "benchmarking_app/views/single_year_graphs.html",
        {"plot": plot, "form": form},
    )


def trend_graphs(request):

    with open(BASE_DIR / "static/SEND_data/sen_phase_type_.csv") as f:
        phase_type = pd.read_csv(f)
    with open(BASE_DIR / "static/SEND_data/stat neighbours.csv") as f:
        stat_neighbours = pd.read_csv(f)

    # data manipulation
    phase_type["ehc_plan_percent_float"] = pd.to_numeric(
        phase_type["ehc_plan_percent"], errors="coerce"
    )
    # phase_type["time_period_str"] = phase_type["time_period"].astype("str")
    phase_type["year"] = phase_type["time_period"].apply(
        lambda x: pd.to_datetime(str(x)[:4], format="%Y") + pd.DateOffset(years=1)
    )

    form = TrendChoice(
        request.POST or None,
        la_choices={
            la: la
            for la in phase_type[phase_type["la_name"].notna()]["la_name"].unique()
        },
        phase_choices={
            phase: phase for phase in phase_type["phase_type_grouping"].unique()
        },
        establishment_choices={
            establishment: establishment
            for establishment in phase_type["type_of_establishment"].unique()
        },
        initial={"phase": "Total", "establishment": "Total"},
    )
    if form.is_valid():
        la_selected = form["la"].value()
        phase_selected = form["phase"].value()
        establishment = form["establishment"].value()
        establishment = [establishment for establishment in establishment]
    else:
        la_selected = "Rochdale"
        phase_selected = "Total"
        establishment = ["Total"]

    phase_slice = phase_type[
        (phase_type["phase_type_grouping"] == phase_selected)
        & (phase_type["type_of_establishment"].isin(establishment))
        & (phase_type["hospital_school"] == "Total")
    ]

    phase_slice["location_name"] = phase_slice.apply(location_picker, axis=1)

    region_selected = phase_slice[phase_slice["la_name"] == la_selected][
        "region_name"
    ].to_list()[0]

    stat_neighbours_list = stat_neighbours[la_selected].to_list()

    phase_slice_neighbours = phase_slice[
        (phase_slice["location_name"] == la_selected)
        | (phase_slice["location_name"] == "England")
        | (phase_slice["location_name"] == region_selected)
    ].copy()

    # We need a location name column for the chart, otherwise la_name values htat are empty (eg the whole of england or a region) don't show up
    phase_slice_neighbours["chart_colour"] = phase_slice_neighbours[
        "location_name"
    ].apply(
        chart_colour_picker,
        la_selected=la_selected,
        region_selected=region_selected,
        stat_neighbours_list=stat_neighbours_list,
    )

    plot = px.line(
        phase_slice_neighbours,
        x="year",
        y="ehc_plan_percent_float",
        color="chart_colour",
        title="Percent of CYP with EHC Plan",
        labels={
            "ehc_plan_percent_float": "Percent of CYP with EHC plan",
            "chart_colour": "",
        },
    )

    plot.update_layout(
        yaxis={
            "categoryorder": "total descending",
        },
        height=700,
    )

    plot = plot.to_html()

    return render(
        request,
        "benchmarking_app/views/trend_graphs.html",
        {"plot": plot, "form": form},
    )


def stat_neighbour_trend_graphs(request):

    with open(BASE_DIR / "static/SEND_data/sen_phase_type_.csv") as f:
        phase_type = pd.read_csv(f)
    with open(BASE_DIR / "static/SEND_data/stat neighbours.csv") as f:
        stat_neighbours = pd.read_csv(f)

    # data manipulation
    phase_type["ehc_plan_percent_float"] = pd.to_numeric(
        phase_type["ehc_plan_percent"], errors="coerce"
    )
    # phase_type["time_period_str"] = phase_type["time_period"].astype("str")
    phase_type["year"] = phase_type["time_period"].apply(
        lambda x: pd.to_datetime(str(x)[:4], format="%Y") + pd.DateOffset(years=1)
    )

    form = TrendChoice(
        request.POST or None,
        la_choices={
            la: la
            for la in phase_type[phase_type["la_name"].notna()]["la_name"].unique()
        },
        phase_choices={
            phase: phase for phase in phase_type["phase_type_grouping"].unique()
        },
        establishment_choices={
            establishment: establishment
            for establishment in phase_type["type_of_establishment"].unique()
        },
        initial={"phase": "Total", "establishment": "Total"},
    )
    if form.is_valid():
        la_selected = form["la"].value()
        phase_selected = form["phase"].value()
        establishment = form["establishment"].value()
        establishment = [establishment for establishment in establishment]
    else:
        la_selected = "Rochdale"
        phase_selected = "Total"
        establishment = ["Total"]

    phase_slice = phase_type[
        (phase_type["phase_type_grouping"] == phase_selected)
        & (phase_type["type_of_establishment"].isin(establishment))
        & (phase_type["hospital_school"] == "Total")
    ]

    phase_slice["location_name"] = phase_slice.apply(location_picker, axis=1)

    region_selected = phase_slice[phase_slice["la_name"] == la_selected][
        "region_name"
    ].to_list()[0]

    stat_neighbours_list = stat_neighbours[la_selected].to_list()

    phase_slice_neighbours = phase_slice[
        (phase_slice["location_name"] == la_selected)
        | (phase_slice["location_name"].isin(stat_neighbours_list))
    ].copy()

    # We need a location name column for the chart, otherwise la_name values htat are empty (eg the whole of england or a region) don't show up
    phase_slice_neighbours["chart_colour"] = phase_slice_neighbours[
        "location_name"
    ].apply(
        chart_colour_picker,
        la_selected=la_selected,
        region_selected=region_selected,
        stat_neighbours_list=stat_neighbours_list,
    )

    plot = px.line(
        phase_slice_neighbours,
        x="year",
        y="ehc_plan_percent_float",
        color="location_name",
        title="Percent of CYP with EHC Plan",
        labels={
            "ehc_plan_percent_float": "Percent of CYP with EHC plan",
            "chart_colour": "",
            "location_name": "",
        },
    )

    plot.update_layout(
        yaxis={
            "categoryorder": "total descending",
        },
        height=700,
    )

    plot = plot.to_html()

    return render(
        request,
        "benchmarking_app/views/stat_neighbour_trend_graphs.html",
        {"plot": plot, "form": form},
    )
