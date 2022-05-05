from django.urls import path, re_path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    re_path(r'^users/(?P<setof>(10|25|50|100))/(?P<num_page>[1-9]\d*)', views.users, name="users"),
]
