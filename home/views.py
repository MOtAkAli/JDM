from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from datetime import datetime
from employee.models import Car, Agency, CarModel, CarBrand, CarType, Reservation
from employee.filters import CarFilter
from user.models import CustomUser
from django.http.response import HttpResponse


class CarListView(ListView):
    model = Car
    template_name = 'home/cars.html'
    paginate_by = 9  # if pagination is desired
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
        startDate = request.POST.get('startDate')
        endDate = request.POST.get('endDate')
        price = request.POST.get('price')
        client = request.POST.get('client')
        client = CustomUser.objects.get(pk=client)
        car = Car.objects.get(pk=car)
        start = datetime.strptime(startDate,'%Y-%m-%d')
        end = datetime.strptime(endDate,'%Y-%m-%d')
        rentdays = end - start
        newprice = float(price)*float(rentdays.days)
        print(type(newprice))
        Reservation.objects.create(start_date=startDate, end_date=endDate, price=newprice, car=car, client=client)
        return HttpResponse(status=200)


def index(request):
    return render(request, 'home/index.html')
