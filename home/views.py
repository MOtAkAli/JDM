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


def login(request):
    return render(request, 'home/login.html')


def register(request):
    if request.method == 'POST':
        password1 = request.POST['password']
        password2 = request.POST['passwordc']
        idn = request.POST['idn']
        form = ClientForm(request.POST)
        print(form.errors)
        if form.is_valid():
            if password1 == password2:
                form.save()
                print("saved..")
                return redirect('/')
            else:
                print("password not matching..")
        else:
            print(form.errors)
    else:
        results = City.objects.all
        return render(request, 'home/register.html', {"Citys": results})
