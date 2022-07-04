from django.urls import path, re_path
from . import views

app_name = 'home'

urlpatterns = [
    path("", views.index, name="index"),
    path('rent/', views.cars_list, name='rent'),
    path('rent/<int:pk>', views.CarDetailView.as_view(), name='car_rent'),
    path('myrents/', views.RentsView.as_view(), name='my_rents'),
]
