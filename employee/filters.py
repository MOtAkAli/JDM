import django_filters
from django import forms
from .models import Car, CarModel, CarType, CarBrand, Agency


class CarFilter(django_filters.FilterSet):  # Do not confuse with the actual car filter
 

    class Meta:
        model = Car
        fields = ['car_model__car_brand','agency__city']
