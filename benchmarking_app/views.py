import pandas as pd

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from send_benchmarking.settings import BASE_DIR

def home(request):

    with open(BASE_DIR / "static/SEND_data/sen_phase_type_.csv") as f:
            phase_type = pd.read_csv(f)

    la_list = phase_type['la_name'].unique()

    return render(
        request,
        "benchmarking_app/views/home.html",
        {"la_list":la_list}
    )


