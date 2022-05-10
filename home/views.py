from django.shortcuts import render
from django.views.generic.list import ListView
from employee.models import Car, Agency,CarModel,CarBrand,CarType
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

        context.update(
            filtered_cars=CarFilter(self.request.GET, queryset=self.model.objects.all())
        )
        context['title'] = ' Rent a car '
        print(context['filtered_cars'].qs)
        return context    


    def get_queryset(self):
        qs = self.model.objects.all().filter(is_active=True,in_use=False)
        filtered_cars = CarFilter(self.request.GET, queryset=qs)
        return filtered_cars.qs

def index(request):
    return render(request, 'home/index.html')