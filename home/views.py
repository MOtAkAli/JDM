from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from employee.models import Car, Agency, CarModel, CarBrand, CarType
from employee.filters import CarFilter


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
        cars = self.model.objects.all().filter(is_active=True, in_use=False)
        carsFilter = CarFilter(self.request.GET, queryset=cars)
        cars = carsFilter.qs

        context["carsFilter"] = carsFilter
        context["cars"] = cars  
        context['title'] = ' Rent a car '
        return context

class CarDetailView(DetailView):

    model= Car
    template_name='home/validationcar.html'
    
    def get_context_data(self, **kwargs):
        context = super(CarDetailView, self).get_context_data(**kwargs)  
        context['title'] = ' Car '+self.object.carModel.name
        return context

    def get_object(self, queryset=None):
        pk = self.kwargs.get("pk")
        car = Car.objects.get(pk=pk)
        return car

def index(request):
    return render(request, 'home/index.html')


def car(request):
    return render(request, 'home/validationcar.html')
