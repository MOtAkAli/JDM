from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    path("", views.index, name="index"),
    path('rent/', views.CarListView.as_view(), name='rent'),
    path('car/', views.car, name='rent'),

]
