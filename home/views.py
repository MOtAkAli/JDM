from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User, auth
from .forms import ClientForm
from employee.models import City
from user.models import CustomUser as Client


def index(request):
    return render(request, 'home/index.html')


def rent(request):
    return render(request, 'home/rent.html')