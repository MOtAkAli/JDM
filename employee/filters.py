import django_filters
from django import forms
from .models import Car, CarModel, CarType, CarBrand,Agency


class CarFilter(django_filters.FilterSet): #Do not confuse with the actual car filter
    CarBrand = django_filters.ModelChoiceFilter(queryset=CarBrand.objects.only('name'),empty_label="All Brands", widget=forms.Select())
    carModel = django_filters.ModelChoiceFilter(queryset=CarModel.objects.only('name'),empty_label="All Models", widget=forms.Select())
    carType = django_filters.ModelChoiceFilter(queryset=CarType.objects.only('name'),empty_label="All Types", widget=forms.Select())
    Agency = django_filters.ModelChoiceFilter(queryset=Agency.objects.only('city.name'),empty_label="All Agencys", widget=forms.Select())
    name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Car
        fields = ['carModel','carType','Agency','name']