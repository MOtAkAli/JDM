from django.contrib.sites.shortcuts import get_current_site
from django.db.models import F
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from datetime import datetime, timedelta
from employee.models import Car, CarBrand, Reservation, CarModel
from cities_light.models import City
from user.models import CustomUser
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.contrib import messages
from django.utils import timezone
from django.conf import settings


def cars_list(request):
    # get car models by car brand using ajax
    if request.method == 'POST':
        car_models = CarModel.objects.filter(car_brand_id=int(request.POST['car_brand_id']))
        return JsonResponse({
            'car_models': [[car_model.id, car_model.name] for car_model in car_models],
        })

    cars = Car.objects.filter(is_active=True)
    cities_cars = cars.values(city_id=F('agency__city_id'), city_name=F('agency__city__name')).distinct()
    car_brands = CarBrand.objects.all()
    car_models = None

    searched_city_id = int(request.GET.get('city', default=City.objects.get(name__contains='Marrakesh').id))
    cars = cars.filter(agency__city_id=searched_city_id)

    searched_car_brand_id = request.GET.get('car_brand', default='')
    if searched_car_brand_id != '':
        car_models = CarModel.objects.filter(car_brand_id=searched_car_brand_id)
        searched_car_brand_id = int(searched_car_brand_id)
        cars = cars.filter(car_model__car_brand_id=searched_car_brand_id)

    searched_car_model_id = request.GET.get('car_model', default='')
    if searched_car_model_id != '':
        searched_car_model_id = int(searched_car_model_id)
        cars = cars.filter(car_model_id=searched_car_model_id)

    return render(
        request,
        'home/cars.html',
        {
            'car_brands': car_brands,
            'searched_car_brand_id': searched_car_brand_id,
            'car_models': car_models,
            'searched_car_model_id': searched_car_model_id,
            'cities_cars': cities_cars,
            'searched_city_id': searched_city_id,
            'cars': cars,
        }
    )


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
        date_intervals = Reservation.objects.filter(car_id=car).filter(start_date__gte=timezone.now()).values(
            'start_date', 'end_date')
        dates = get_dates_from_intervals(
            [[date_interval['start_date'], date_interval['end_date']] for date_interval in date_intervals])
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
                rentdays = rentdays.days + 1
                newprice = float(price) * float(rentdays)
                Reservation.objects.create(
                    start_date=startDate,
                    end_date=endDate,
                    price=newprice,
                    car=car,
                    client=client
                )
                domain = get_current_site(request).domain
                my_rents_url = request.scheme + '://' + domain + '/myrents/'
                email_body = render_to_string('home/rent_notification_body.html', {
                    'car_model': car.car_model,
                    'days': rentdays,
                    'start': start,
                    'end': end,
                    'my_rents_url': my_rents_url,
                })
                email = EmailMultiAlternatives(
                    subject='Rent Notification',
                    body=f'Your rend of {car.car_model} for {rentdays} days from {start} to {end} has been created\n'
                         f'And we will inform you by email you when it is confirmed'
                         f'Check {my_rents_url} for details',
                    from_email=settings.EMAIL_HOST_USER,
                    to=(request.user.email,)
                )
                email.attach_alternative(email_body, "text/html")
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
