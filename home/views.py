from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User, auth
from .models import *
from .forms import ClientForm

def index(request):
    return render(request, 'home/index.html')


def rent(request):
    return render(request, 'home/rent.html')


def login(request):
    return render(request, 'home/login.html')


def register(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        print(form.errors)
        if form.is_valid():
            form.save()
            print("saved")
        return redirect('/')
    else:
        return render(request, 'home/register.html')
