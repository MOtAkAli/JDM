from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns = [
    path("", views.index, name="index"),
    path("cars",views.cars, name="cars"),
    path("cars/details",views.details ,name="details"),
    path("details.html",views.details ,name="details"),


]
urlpatterns += staticfiles_urlpatterns()