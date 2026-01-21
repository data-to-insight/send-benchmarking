from django.urls import path

from benchmarking_app import views

urlpatterns = [
    path("", views.home, name="Home"),
    path("single_year_graphs", views.single_year_graphs, name="single_year_graphs"),
    path(
        "select_ehcp_dataset",
        views.select_ehcp_dataset,
        name="select_ehcp_dataset",
    ),
    path(
        "single_year_ehcp_graphs",
        views.single_year_ehcp_graphs,
        name="single_year_ehcp_graphs",
    ),
    path("trend_graphs", views.trend_graphs, name="trend_graphs"),
    path(
        "stat_neighbour_trend_graphs",
        views.stat_neighbour_trend_graphs,
        name="stat_neighbour_trend_graphs",
    ),
]
