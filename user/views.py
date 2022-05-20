from django.shortcuts import render, redirect
from .forms import UserRegisterForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.contrib.auth import login as auth_login
from cities_light.models import City
from django.core.mail import EmailMessage

User = get_user_model()


def register(request):
    results = City.objects.all
    if request.user.is_authenticated:
        messages.warning(request, f'Your are already logged in')
        return render(request, '/')
    else:
        if request.method == 'POST':
            form = UserRegisterForm(request.POST,request.FILES,)
            if form.is_valid():
                user = form.save(commit=False)
                username = form.cleaned_data.get('username')
                user.save()
                email = EmailMessage(
                    'JDM no reply',
                    'Welcome to JDM !!!!!!!!!',
                    'jdmrent2022@gmail.com',
                    [user.email],
                )
                email.send(fail_silently=False)
                messages.success(request, f'Your account has been successfully created.Check your mail')
                return redirect('/')
        else:
            form = UserRegisterForm()
        messages.error(request, form.errors)
        return render(request, 'user/register.html', {'form': form, "City": results})


class LoginView(LoginView):
    template_name = 'user/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        username = form.get_user()
        user = User.objects.get(username=username)
        if user.is_active:
            auth_login(self.request, form.get_user())
            messages.success(self.request, f'You are now logged in as {user.username}')
            return redirect('/')
