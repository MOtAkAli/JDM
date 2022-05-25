from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from datetime import datetime, timedelta
from employee.models import Car, Agency, CarModel, CarBrand, CarType, Reservation
from employee.filters import CarFilter
from user.models import CustomUser
from django.core.mail import EmailMessage
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone


class CarListView(ListView):
    model = Car
    template_name = 'home/cars.html'
    paginate_by = 4  # if pagination is desired
    context_object_name = 'cars'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["brands"] = CarBrand.objects.all()
        context["types"] = CarType.objects.all()
        context["CarModel"] = CarModel.objects.all()
        cars = self.model.objects.all().filter(is_active=True)
        carsFilter = CarFilter(self.request.GET, queryset=cars)
        cars = carsFilter.qs

        context["carsFilter"] = carsFilter
        context["cars"] = cars
        context['title'] = ' Rent a car '
        return context


def date_range(start, end):
    delta = end - start
    days = [start + timedelta(days=i) for i in range(delta.days + 1)]
    return days


def get_dates_from_intervals(date_intervals):
    dates = []
    for date_interval in date_intervals:
        for date in date_range(date_interval[0], date_interval[1]):
            dates.append(date)
    return dates


class CarDetailView(DetailView):
    model = Car
    template_name = 'home/validationcar.html'

    def get_context_data(self, **kwargs):
        context = super(CarDetailView, self).get_context_data(**kwargs)
        context['title'] = ' Car ' + self.object.car_model.name
        return context

    def get_object(self, queryset=None):
        pk = self.kwargs.get("pk")
        car = Car.objects.get(pk=pk)
        return car

    def post(self, request, *args, **kwargs):
        car = request.POST.get('car')
        date_intervals = Reservation.objects.filter(car_id=car).filter(start_date__gte=timezone.now()).values('start_date', 'end_date')
        dates = get_dates_from_intervals([[date_interval['start_date'], date_interval['end_date']] for date_interval in date_intervals])
        if request.POST.get('need'):
            return JsonResponse({
                'dates': dates,
            })
        else:
            startDate = request.POST.get('startDate').split('/')
            startDate = startDate[2] + '-' + startDate[0] + '-' + startDate[1]
            endDate = request.POST.get('endDate').split('/')
            endDate = endDate[2] + '-' + endDate[0] + '-' + endDate[1]
            start = datetime.strptime(startDate, '%Y-%m-%d').date()
            end = datetime.strptime(endDate, '%Y-%m-%d').date()
            error = False
            if start < timezone.now().date() or end < timezone.now().date() or not start < end:
                error = True
                return JsonResponse({
                    'error': 'Invalid date',
                })
            if start in dates or end in dates:
                error = True
                return JsonResponse({
                    'error': 'Reservation date already taken',
                })
            price = request.POST.get('price')
            client = request.POST.get('client')
            client = CustomUser.objects.get(pk=client)
            car = Car.objects.get(pk=car)
            if not error:
                rentdays = end - start
                newprice = float(price) * float(rentdays.days)
                Reservation.objects.create(
                    start_date=startDate,
                    end_date=endDate,
                    price=newprice,
                    car=car,
                    client=client
                )
                email = EmailMessage(
                    'JDM no reply',
                    'RENT DONE  !! check My rents',
                    'jdmrent2022@gmail.com',
                    [client.email],
                )
                email.send(fail_silently=False)
                messages.success(self.request, f'rent done')
            return redirect('home:index')


class RentsView(ListView):
    model = Reservation
    paginate_by = 10  # if pagination is desired
    template_name = 'home/my_rents.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self):
        queryset = Reservation.objects.filter(client=self.request.user)
        return queryset


def index(request):
    return render(request, 'home/index.html')
