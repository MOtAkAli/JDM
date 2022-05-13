from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from django.core.paginator import Paginator
from user.models import *


def index(request):
    return render(request, 'employee/index.html', {})


def reservations(request, setof, num_page):
    reservations = Reservation.objects.all()
    paginator = Paginator(reservations, setof)
    reservations_page = paginator.get_page(num_page)
    return render(request, 'employee/reservations.html',
                  {
                   "reservations_page": reservations_page,
                   "count": paginator.count,
                   "page_has_previous": reservations_page.has_previous,
                   "page_has_next": reservations_page.has_next,
                   "setof": int(setof),
                   "num_page_previous": int(num_page) - 1,
                   "num_page": int(num_page),
                   "num_page_next": int(num_page) + 1,
                   })


def reservation(request, id):
    reservation = Reservation.objects.get(id=id)
    return render(request, 'employee/reservation.html',
                  {"reservation": reservation,
                   })
