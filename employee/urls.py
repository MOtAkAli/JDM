from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("reservations/<int:setof>/<int:num_page>", views.reservations, name="reservations"),
    path("reservation/<int:id>", views.reservation, name="details"),
]
