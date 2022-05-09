from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns = [
    path("", views.index, name="index"),
    path("cars",views.cars, name="cars"),
    path("cars/details",views.details ,name="details"),
    path("details.html",views.details ,name="details"),
    path("cars/details/<int:id>",views.details_with_id ,name="details_with_id"),
    path("details.html/<int:id>",views.details_with_id ,name="details_with_id"),
]
urlpatterns += staticfiles_urlpatterns()