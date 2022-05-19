from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator
from .models import Reservation
from django.db.models import Avg
from django.db.models.functions import TruncMonth, TruncYear
import calendar
from user.models import CustomUser, Role


def monthly_earnings_list(monthly_earnings):
    earnings = {}
    for monthly_earning in monthly_earnings:
        earnings[calendar.month_name[monthly_earning['month'].month]] = monthly_earning['count']
    return earnings


def annually_earnings_list(annually_earnings):
    earnings = {}
    for annually_earning in annually_earnings:
        earnings[annually_earning['year'].year] = annually_earning['count']
    return earnings


def avg_earnings(earnings_list):
    sum_earnings = 0
    for earning in earnings_list:
        sum_earnings += earning
    return 0 if len(earnings_list) == 0 else int(sum_earnings / len(earnings_list))


def index(request):
    reservations = Reservation.objects.all()
    if request.method == 'POST':
        if request.POST['which_one'] == 'reservations':
            monthly_earnings = monthly_earnings_list(
                reservations.
                    filter(paid=True).
                    filter(start_date__year=request.POST['year']).
                    annotate(month=TruncMonth('start_date')).
                    values('month').annotate(count=Avg('price'))
            )
            return JsonResponse(
                {
                    'months': list(monthly_earnings.keys()),
                    'monthly_earnings': list(monthly_earnings.values()),
                    'monthly_earning': avg_earnings(monthly_earnings.values()),
                }
            )
    #
    annually_earnings = annually_earnings_list(
        reservations.
            filter(paid=True).
            annotate(year=TruncYear('start_date')).
            values('year').
            annotate(count=Avg('price'))
    )
    years = [year for year in reversed(annually_earnings.keys())]
    annually_earnings = [annually_earnings for annually_earnings in reversed(annually_earnings.values())]
    #
    monthly_earnings = monthly_earnings_list(
        reservations.
            filter(paid=True).
            filter(start_date__year=years[0]).
            annotate(month=TruncMonth('start_date')).
            values('month').
            annotate(count=Avg('price'))
    )
    months = monthly_earnings.keys()
    monthly_earnings = monthly_earnings.values()
    #
    return render(
        request,
        'employee/index.html',
        {
            'months': months,
            'monthly_earnings': monthly_earnings,
            'reservations_monthly_earning': avg_earnings(monthly_earnings),
            'years': years,
            'annually_earnings': annually_earnings,
            'reservations_annually_earning': avg_earnings(annually_earnings),
            'reservations_count': reservations.count(),
            'verified_reservations_count': reservations.filter(confirmed=True).count(),
        }
    )


def users(request, search, setof, num_page):
    if request.method == 'POST':
        try:
            user = CustomUser.objects.get(id=int(request.POST['id']))
            user.is_active = bool(int(request.POST['is_active']))
            user.inactive_reason = request.POST['reason'] if not user.is_active else ''
            user.save()
            return JsonResponse({
                'is_active': user.is_active,
            })
        except CustomUser.DoesNotExist:
            return JsonResponse({
                'error_msg': 'user does not exist',
            })

    search = search.split('=')

    users = CustomUser.objects. \
        exclude(is_superuser=True). \
        exclude(is_staff=True). \
        exclude(roles__in=Role.objects.filter(name__in=('CM', 'RM', 'VM'))). \
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
            'search_filter': search[0] if len(search) == 2 else '',
            'search_value': search[1] if len(search) == 2 else '',
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
    reservations = Reservation.objects.all()

    search = search.split('=')

    if search[0] == 'id':
        reservations = reservations.filter(client__idn__contains=search[1])
    elif search[0] == 'first_name':
        reservations = reservations.filter(client__first_name__icontains=search[1])
    elif search[0] == 'last_name':
        reservations = reservations.filter(client__last_name__contains=search[1])
    elif search[0] == 'email':
        reservations = reservations.filter(client__email__contains=search[1])
    elif search[0] == 'phone':
        reservations = reservations.filter(client__phone__contains=search[1])

    paginator = Paginator(reservations, setof)
    reservations_page = paginator.get_page(num_page)
    if int(num_page) > paginator.num_pages:
        num_page = paginator.num_pages
    return render(request, 'employee/reservations.html',
                  {
                   'search_filter': search[0] if len(search) == 2 else '',
                   'search_value': search[1] if len(search) == 2 else '',
                   'search_is_active': True if len(search)==2 else False,
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
