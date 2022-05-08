from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from user.models import CustomUser, Role
from django.core.paginator import Paginator


def index(request):
    return render(request, 'employee/index.html', {})


def users(request, search, setof, num_page):
    if request.method == 'POST':
        print(request.POST)
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
