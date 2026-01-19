import pandas as pd
import plotly.express as px

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from send_benchmarking.settings import BASE_DIR
from benchmarking_app.forms import PhaseEstablishmentChoice, LAYearChoice

from benchmarking_app.utils import chart_colour_picker, location_picker


def home(request):

    with open(BASE_DIR / "static/SEND_data/sen_phase_type_.csv") as f:
        phase_type = pd.read_csv(f)

        form = PhaseEstablishmentChoice(
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
    ]

    phase_slice["location_name"] = phase_slice.apply(location_picker, axis=1)
    region_selected = phase_slice[phase_slice["la_name"] == la_selected][
        "region_name"
    ].to_list()[0]

    # We need a location name column for the chart, otherwise la_name values htat are empty (eg the whole of england or a region) don't show up
    phase_slice["chart_colour"] = phase_slice["location_name"].apply(
        chart_colour_picker, la_selected=la_selected, region_selected=region_selected
    )

    plot = px.bar(
        phase_slice, x="location_name", y="ehc_plan_percent", color="chart_colour"
    ).to_html()

    return render(
        request, "benchmarking_app/views/home.html", {"plot": plot, "form": form}
    )
