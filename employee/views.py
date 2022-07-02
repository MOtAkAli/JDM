from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import HttpResponse, JsonResponse
from user.models import CustomUser, Role, RoleEnum
from django.core.paginator import Paginator

from user.views import get_custom_user_roles
from .models import Reservation, Car, CarType, PaymentLog, EmployeeLog, CarBrand, CarModel
from django.db.models import Avg, Count
from django.db.models.functions import TruncMonth, TruncYear
import calendar


def monthly_earnings_dict(monthly_earnings):
    earnings = {
        'January': 0,
        'February': 0,
        'March': 0,
        'April': 0,
        'May': 0,
        'June': 0,
        'July': 0,
        'August': 0,
        'September': 0,
        'October': 0,
        'November': 0,
        'December': 0,
    }
    for monthly_earning in monthly_earnings:
        earnings[calendar.month_name[monthly_earning['month'].month]] = monthly_earning['avg']
    return earnings


def annually_earnings_dict(annually_earnings):
    earnings = {}
    for annually_earning in annually_earnings:
        earnings[annually_earning['year'].year] = annually_earning['avg']
    return earnings


def avg_earnings(earnings_list, count):
    sum_earnings = 0
    for earning in earnings_list:
        sum_earnings += earning
    return 0 if count == 0 else int(sum_earnings / count)


def cars_count_by_type_dict(cars_count_by_type):
    types_count = {}
    car_types = dict(CarType.CAR_TYPES)
    for car_count_by_type in cars_count_by_type:
        types_count[car_types.get(
            car_count_by_type['car_type__name'])] = car_count_by_type['count']
    return types_count


def cars_count_by_brand_dict(cars_count_by_brand):
    brands_count = {}
    for car_count_by_brand in cars_count_by_brand:
        brands_count[car_count_by_brand['car_model__car_brand__name']] = car_count_by_brand['count']
    return brands_count


def users_count_by_cities_dict(users_count_by_cities):
    cities_counts = {}
    for user_count_by_city in users_count_by_cities:
        cities_counts[user_count_by_city['city__name']] = user_count_by_city['count']
    return cities_counts


def index(request):
    # check user
    if not request.user.is_authenticated:
        return redirect('user:login')
    user_roles = get_custom_user_roles(request.user.id)
    if request.user.is_superuser:
        return redirect('/admin/')
    if not user_roles['is_client_manager'] or not user_roles['is_reservation_manager'] or not user_roles['is_vehicle_manager']:
        return redirect('home:index')
    # get all()
    reservations = Reservation.objects.all()
    cars = Car.objects.all()
    users = CustomUser.objects. \
        exclude(is_superuser=True). \
        exclude(is_staff=True). \
        exclude(roles__in=Role.objects.filter(
        name__in=(
            RoleEnum.CLIENT_MANAGER.value,
            RoleEnum.RESERVATION_MANAGER.value,
            RoleEnum.VEHICLE_MANAGER.value,
        )
    )
    )
    # ajax reservations stats by year
    if request.method == 'POST':
        if request.POST['which_one'] == 'reservations':
            monthly_earnings = monthly_earnings_dict(
                reservations.
                    filter(paid=True).
                    filter(start_date__year=request.POST['year']).
                    annotate(month=TruncMonth('start_date')).
                    values('month').annotate(avg=Avg('price'))
            )
            return JsonResponse(
                {
                    'months': list(monthly_earnings.keys()),
                    'monthly_earnings': list(monthly_earnings.values()),
                    'monthly_earning': avg_earnings(monthly_earnings.values(), len(monthly_earnings.values())),
                }
            )
    # reservations / annually_earnings
    annually_earnings = annually_earnings_dict(
        reservations.
            filter(paid=True).
            annotate(year=TruncYear('start_date')).
            values('year').
            annotate(avg=Avg('price'))
    )
    years = [year for year in reversed(annually_earnings.keys())]
    max_year = 0 if len(years) == 0 else max(years)
    min_year = 0 if len(years) == 0 else min(years)
    annually_earnings = [annually_earnings for annually_earnings in reversed(
        annually_earnings.values())]
    # reservations / monthly_earnings
    monthly_earnings = monthly_earnings_dict(
        reservations.
            filter(paid=True).
            filter(start_date__year=years[0] if len(years) > 0 else None).
            annotate(month=TruncMonth('start_date')).
            values('month').
            annotate(avg=Avg('price'))
    )
    months = monthly_earnings.keys()
    monthly_earnings = monthly_earnings.values()
    # car brands counts
    cars_count_by_brand = cars_count_by_brand_dict(
        cars.values('car_model__car_brand__name').annotate(
            count=Count('car_model__car_brand__name'))
    )
    # car types counts
    cars_count_by_type = cars_count_by_type_dict(
        cars.values('car_type__name').annotate(count=Count('car_type__name'))
    )
    # user cities counts
    users_count_by_cities = users_count_by_cities_dict(
        users.values('city__name').annotate(count=Count('city__name'))
    )
    return render(
        request,
        'employee/index.html',
        {
            # employee
            'employee_name': request.user.first_name + ' ' + request.user.last_name,
            'employee_avatar_url': CustomUser.objects.get(id=request.user.id).picture.url,
            'is_client_manager': user_roles['is_client_manager'],
            'is_reservation_manager': user_roles['is_reservation_manager'],
            'is_vehicle_manager': user_roles['is_vehicle_manager'],
            # reservations stats
            'months': months,
            'monthly_earnings': monthly_earnings,
            'reservations_monthly_earning': avg_earnings(monthly_earnings, len(monthly_earnings)),
            'years': years,
            'annually_earnings': annually_earnings,
            'reservations_annually_earning': avg_earnings(annually_earnings, max_year - min_year + 1),
            'reservations_count': reservations.count(),
            'paid_reservations_count': reservations.filter(paid=True).count(),
            # cars stats
            'cars_count': cars.count(),
            'active_cars_count': cars.filter(is_active=True).count(),
            'inactive_cars_count': cars.filter(is_active=False).count(),
            'car_brands': cars_count_by_brand.keys(),
            'car_brands_counts': cars_count_by_brand.values(),
            'car_types': cars_count_by_type.keys(),
            'car_types_counts': cars_count_by_type.values(),
            # users
            'users_count': users.count(),
            'active_users_count': users.filter(is_active=True).count(),
            'inactive_users_count': users.filter(is_active=False).count(),
            'users_cities': users_count_by_cities.keys(),
            'cities_counts': users_count_by_cities.values(),
        }
    )


def users(request, search, setof, num_page):
    # check user
    if not request.user.is_authenticated:
        return redirect('user:login')
    user_roles = get_custom_user_roles(request.user.id)
    if not user_roles['is_client_manager']:
        return redirect('index')
    # ajax update user is_active
    if request.method == 'POST':
        try:
            client_id = int(request.POST['id'])
            client = CustomUser.objects.get(id=client_id)
            new_is_active = bool(int(request.POST['is_active']))
            client.is_active = new_is_active
            client.save()
            EmployeeLog(
                description='Client account ' +
                            ('activated' if client.is_active else 'deactivated'),
                status_reason=request.POST['reason'],
                employee_id=request.user.id,
                client_id=client_id,
            ).save()
            return JsonResponse({
                'is_active': client.is_active,
            })
        except CustomUser.DoesNotExist:
            return JsonResponse({
                'error_msg': 'user does not exist',
            })
    # split search
    search = search.split('=')
    # users
    users = CustomUser.objects. \
        exclude(is_superuser=True). \
        exclude(is_staff=True). \
        exclude(
        roles__in=Role.objects.filter(
            name__in=(
                RoleEnum.CLIENT_MANAGER.value,
                RoleEnum.RESERVATION_MANAGER.value,
                RoleEnum.VEHICLE_MANAGER.value
            )
        )
    ). \
        order_by('id')

    if search[0] == 'id':
        users = users.filter(idn__contains=search[1])
    elif search[0] == 'first_name':
        users = users.filter(first_name__contains=search[1])
    elif search[0] == 'last_name':
        users = users.filter(last_name__contains=search[1])
    elif search[0] == 'email':
        users = users.filter(email__contains=search[1])
    elif search[0] == 'phone':
        users = users.filter(phone__contains=search[1])

    paginator = Paginator(users, setof)
    if int(num_page) > paginator.num_pages:
        num_page = paginator.num_pages
    users_page = paginator.get_page(num_page)
    return render(
        request,
        'employee/users.html',
        {
            # employee
            'employee_name': request.user.first_name + ' ' + request.user.last_name,
            'employee_avatar_url': CustomUser.objects.get(id=request.user.id).picture.url,
            'is_client_manager': user_roles['is_client_manager'],
            'is_reservation_manager': user_roles['is_reservation_manager'],
            'is_vehicle_manager': user_roles['is_vehicle_manager'],
            # users
            'search_filter': search[0] if len(search) == 2 else '',
            'search_value': search[1] if len(search) == 2 else '',
            'search_is_active': True if len(search) == 2 else False,
            'users_page': users_page,
            'count': paginator.count,
            'page_has_previous': users_page.has_previous,
            'page_has_next': users_page.has_next,
            'setof': int(setof),
            'num_page_previous': int(num_page) - 1,
            'num_page': int(num_page),
            'num_page_next': int(num_page) + 1,
        }
    )


def reservations(request, search, setof, num_page):
    # check user
    if not request.user.is_authenticated:
        return redirect('user:login')
    user_roles = get_custom_user_roles(request.user.id)
    if not user_roles['is_reservation_manager']:
        return redirect('index')
    #
    reservations = Reservation.objects.all()

    if request.method == 'POST':
        try:
            reservation = reservations.get(id=int(request.POST['id']))
            if reservation.confirmed:
                reservation.paid = True
                reservation.save()
                EmployeeLog(
                    description='Reservation have been paid',
                    status_reason='Client paid the reservation',
                    employee_id=request.user.id,
                    reservation_id=reservation.id,
                ).save()
                PaymentLog(
                    reservation_id=reservation.id,
                    employee_id=request.user.id,
                ).save()
                return JsonResponse({
                    'reservation_is_paid': reservation.paid,
                })
            else:
                return JsonResponse({
                    'error': 'reservation already paid',
                })
        except Reservation.DoesNotExist:
            return JsonResponse({
                'error': 'reservation not found',
            })

    search = search.split('=')

    if search[0] == 'id':
        reservations = reservations.filter(client__idn__contains=search[1])
    elif search[0] == 'first_name':
        reservations = reservations.filter(client__first_name__contains=search[1])
    elif search[0] == 'last_name':
        reservations = reservations.filter(client__last_name__contains=search[1])
    elif search[0] == 'email':
        reservations = reservations.filter(client__email__contains=search[1])
    elif search[0] == 'phone':
        reservations = reservations.filter(client__phone__contains=search[1])

    paginator = Paginator(reservations.order_by('created_at'), setof)
    reservations_page = paginator.get_page(num_page)
    if int(num_page) > paginator.num_pages:
        num_page = paginator.num_pages
    return render(
        request,
        'employee/reservations.html',
        {
            # employee
            'employee_name': request.user.first_name + ' ' + request.user.last_name,
            'employee_avatar_url': CustomUser.objects.get(id=request.user.id).picture.url,
            'is_client_manager': user_roles['is_client_manager'],
            'is_reservation_manager': user_roles['is_reservation_manager'],
            'is_vehicle_manager': user_roles['is_vehicle_manager'],
            #
            'search_filter': search[0] if len(search) == 2 else '',
            'search_value': search[1] if len(search) == 2 else '',
            'search_is_active': True if len(search) == 2 else False,
            "reservations_page": reservations_page,
            "count": paginator.count,
            "page_has_previous": reservations_page.has_previous,
            "page_has_next": reservations_page.has_next,
            "setof": int(setof),
            "num_page_previous": int(num_page) - 1,
            "num_page": int(num_page),
            "num_page_next": int(num_page) + 1,
        }
    )


def reservation(request, id):
    # check user
    if not request.user.is_authenticated:
        return redirect('user:login')
    user_roles = get_custom_user_roles(request.user.id)
    if not user_roles['is_reservation_manager']:
        return redirect('index')
    # get reservation by id
    reservation = Reservation.objects.get(id=id)
    # check if reservation is not affected to any user
    if not reservation.employee_id:
        reservation.employee_id = request.user.id
        reservation.save()
        EmployeeLog(
            description='Reservation have been affected to',
            status_reason='Reservation will be taken by',
            employee_id=request.user.id,
        ).save()
    # check if reservation ownership
    if reservation.employee_id != request.user.id:
        return redirect('/employee/reservations/search//10/1')
    # to be replaced by ajax
    if request.method == 'POST':
        if reservation.paid:
            return JsonResponse({
                'error': 'You can\'t unconfirme a paid reservation',
            })

        reservation.confirmed = not reservation.confirmed
        reservation.save()
        EmployeeLog(
            description='Reservation have been ' + ('confirmed' if reservation.confirmed else 'unconfirmed'),
            status_reason=request.POST['reason'],
            employee_id=request.user.id,
            reservation_id=reservation.id,
        ).save()
        return JsonResponse({
            'confirmed': reservation.confirmed,
        })

    return render(
        request,
        'employee/reservation.html',
        {
            # employee
            'employee_name': request.user.first_name + ' ' + request.user.last_name,
            'employee_avatar_url': CustomUser.objects.get(id=request.user.id).picture.url,
            'is_client_manager': user_roles['is_client_manager'],
            'is_reservation_manager': user_roles['is_reservation_manager'],
            'is_vehicle_manager': user_roles['is_vehicle_manager'],
            #
            "reservation": reservation,
        }
    )


def cars(request, search, setof, num_page):
    # check user
    if not request.user.is_authenticated:
        return redirect('user:login')
    user_roles = get_custom_user_roles(request.user.id)
    if not user_roles['is_vehicle_manager']:
        return redirect('index')
    # get models by brand using ajax
    if request.method == 'POST':
        car_models = CarModel.objects.all().filter(car_brand_id=int(request.POST['brand_id']))
        return JsonResponse({
            'car_models': [[car_model.id, car_model.name] for car_model in car_models],
        })
    #
    cars = Car.objects.all()

    car_brands = CarBrand.objects.all()

    search = search.split('&')

    registration_number_search = ''
    brand_search = None
    model_search = None
    car_models = None
    is_search = False

    if len(search) == 3:
        registration_number_search = search[0].split('=')[1]
        brand_search = search[1].split('=')[1]
        model_search = search[2].split('=')[1]
        #
        cars = cars.filter(registration_number__contains=registration_number_search)
        if brand_search:
            brand_search = int(brand_search)
            cars = cars.filter(car_model__car_brand_id=brand_search)
            car_models = CarModel.objects.all().filter(car_brand_id=brand_search)
        if model_search:
            model_search = int(model_search)
            cars = cars.filter(car_model_id=model_search)
        is_search = True

    paginator = Paginator(cars.order_by('id'), setof)
    cars_page = paginator.get_page(num_page)
    if int(num_page) > paginator.num_pages:
        num_page = paginator.num_pages

    return render(
        request,
        'employee/cars.html',
        {
            # employee
            'employee_name': request.user.first_name + ' ' + request.user.last_name,
            'employee_avatar_url': CustomUser.objects.get(id=request.user.id).picture.url,
            'is_client_manager': user_roles['is_client_manager'],
            'is_reservation_manager': user_roles['is_reservation_manager'],
            'is_vehicle_manager': user_roles['is_vehicle_manager'],
            # search
            'is_search': is_search,
            'registration_number_search': registration_number_search,
            'brand_search': brand_search,
            'model_search': model_search,
            #
            'car_models': car_models,
            'car_brands': car_brands,
            'cars_page': cars_page,
            'count': paginator.count,
            'page_has_previous': cars_page.has_previous,
            'page_has_next': cars_page.has_next,
            'setof': int(setof),
            'num_page_previous': int(num_page) - 1,
            'num_page': int(num_page),
            'num_page_next': int(num_page) + 1,
        }
    )


def car(request, id):
    # check user
    if not request.user.is_authenticated:
        return redirect('user:login')
    user_roles = get_custom_user_roles(request.user.id)
    if not user_roles['is_vehicle_manager']:
        return redirect('index')
    #
    car = Car.objects.get(id=id)

    if request.method == 'POST':
        car.is_active = not car.is_active
        car.save()
        EmployeeLog(
            description='Car have been ' + ('activated' if car.is_active else 'deactivated'),
            status_reason=request.POST['reason'],
            employee_id=request.user.id,
            car_id=car.id,
        ).save()
        return JsonResponse({
            'is_active': car.is_active,
        })
    return render(
        request,
        'employee/car.html',
        {
            # employee
            'employee_name': request.user.first_name + ' ' + request.user.last_name,
            'employee_avatar_url': CustomUser.objects.get(id=request.user.id).picture.url,
            'is_client_manager': user_roles['is_client_manager'],
            'is_reservation_manager': user_roles['is_reservation_manager'],
            'is_vehicle_manager': user_roles['is_vehicle_manager'],
            #
            'car': car,
        }
    )
