from django.urls import path, re_path
from . import views

app_name = 'employee'

urlpatterns = [
    path('', views.index, name='index'),
    re_path(
        r'^users/search/(?P<search>((id|first_name|last_name|email|phone)=(\w+[\-\.]*\w+@?\w+\-?\w+\.?\w+|\w+))?)/(?P<setof>(10|25|50|100))/(?P<num_page>[1-9]\d*)',
        views.users, name='users'),
    re_path(
        r'^reservations/search/(?P<search>((id|first_name|last_name|email|phone)=(\w+[\-\.]*\w+@?\w+\-?\w+\.?\w+|\w+))?)/(?P<setof>(10|25|50|100))/(?P<num_page>[1-9]\d*)',
        views.reservations, name='reservations'),
    re_path(
        r'^cars/search/(?P<search>((registration_number=\w*&brand=\d*&model=\d*)?))/(?P<setof>(10|25|50|100))/(?P<num_page>[1-9]\d*)',
        views.cars, name='cars'),
    path("reservation/<int:id>", views.reservation, name="details"),
    path("cars/<int:setof>/<int:num_page>", views.cars, name="cars"),
    path("car/<int:id>", views.car, name="car"),
]
