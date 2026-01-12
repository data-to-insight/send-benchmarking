from django.urls import path

from benchmarking_app import views

urlpatterns = [
    path("", views.home, name="home"),
]