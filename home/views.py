from django.shortcuts import render


def index(request):
    return render(request, 'home/index.html')


def rent(request):
    return render(request, 'home/rent.html')
