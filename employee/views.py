from django.shortcuts import render
from django.http import HttpResponse
from user.models import User
from django.core.paginator import Paginator


def index(request):
    return render(request, 'employee/index.html', {})


def users(request, setof, num_page):
    users = User.objects.all().order_by('id')
    paginator = Paginator(users, setof)
    users_page = paginator.get_page(num_page)
    return render(
        request,
        'employee/users.html',
        {'users_page': users_page,
         'count': paginator.count,
         'nums_pages': paginator.page_range,
         'page_has_previous': users_page.has_previous,
         'page_has_next': users_page.has_next,
         'setof': int(setof),
         'num_page_previous': int(num_page) - 1,
         'num_page': int(num_page),
         'num_page_next': int(num_page) + 1,
         }
    )
