from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return render(request, 'home/index.html')


def rent(request):
    return render(request, 'home/rent.html')


def login(request):
    return render(request, 'home/login.html')


def register(request):
    return render(request, 'home/register.html')
