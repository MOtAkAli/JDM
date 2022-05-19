from django.urls import path, re_path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    re_path(
        r'^reservations/search/(?P<search>((id|first_name|last_name|email|phone)=(\w+[\-\.]*\w+@?\w+\-?\w+\.?\w+|\w+))?)/(?P<setof>(10|25|50|100))/(?P<num_page>[1-9]\d*)',
        views.reservations, name='users'),
    path("reservation/<int:id>", views.reservation, name="details"),
]
