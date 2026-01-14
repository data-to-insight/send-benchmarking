import pandas as pd
import plotly.express as px

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from send_benchmarking.settings import BASE_DIR
from send_benchmarking.forms import PhaseEstablishmentChoice


def home(request):

    with open(BASE_DIR / "static/SEND_data/sen_phase_type_.csv") as f:
        phase_type = pd.read_csv(f)

    form = PhaseEstablishmentChoice(
        request.POST or None,
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
        phase_selected = int(form["year"].value())
        establishment = form["placement"].value()
    else:
        phase_selected = "Total"
        establishment = "Total"

    phase_slice = phase_type[
        (phase_type["phase_type_grouping"] == "Total")
        & (phase_type["type_of_establishment"] == "Total")
        & (phase_type["time_period"].astype("str") == "202425")
    ]

    plot = px.bar(phase_slice, x="la_name", y="ehc_plan_percent").to_html()

    return render(
        request, "benchmarking_app/views/home.html", {"plot": plot, "form": form}
    )
