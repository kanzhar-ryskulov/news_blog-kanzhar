from django.urls import path

from api_v1.views import json_echo_view, add, subtract, multiply, divide

urlpatterns = [
    path("echo/", json_echo_view, name="list"),
    path("add/", add),
    path("subtract/", subtract),
    path("multiply/", multiply),
    path("divide/", divide)
]