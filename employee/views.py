from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from user.models import *


def index(request):
    return render(request, 'employee/index.html', {})


def reservations(request):
    obj = Reservation.objects.all()
    return render(request, 'employee/reservations.html', {"obj": obj})


def reservation(request, id):
    reservation = Reservation.objects.get(id=id)
    return render(request, 'employee/reservation.html', {"reservation": reservation})
