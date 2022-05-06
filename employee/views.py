from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return render(request, 'employee/index.html', {})

def cars(request):
    return render(request, 'employee/cars.html', {})
