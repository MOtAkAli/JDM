from unicodedata import name
from django.shortcuts import render
from django.http import HttpResponse
from . models import CarBrand , CarType , CarModel , Car
 

def index(request):
    return render(request, 'employee/index.html', {})

def cars(request):
    cars_data_base= Car.objects.all()
  

    return render(request, 'employee/cars.html', {'cars_data_base':cars_data_base })


def details(request):
        cars_data_base= Car.objects.all()
        return render(request, 'employee/details.html', {'cars_data_base':cars_data_base })
    
  

    
