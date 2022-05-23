from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import UserRegisterForm, UserUpdateForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.contrib.auth import login as auth_login
from cities_light.models import City
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from user.models import CustomUser
from uuid import uuid4

User = get_user_model()


def register(request):
    results = City.objects.all
    if request.user.is_authenticated:
        messages.warning(request, f'Your are already logged in')
        return render(request, '/')
    else:
        if request.method == 'POST':
            form = UserRegisterForm(request.POST, request.FILES, )
            if form.is_valid():
                user = form.save(commit=False)
                user.email_token = uuid4()
                user.save()
                domain = get_current_site(request).domain
                activate_url = 'http://' + domain + '/user/email-verification/' + str(user.email_token)
                email_body = 'Welcome ' + user.username + ' Please verify your account\n ' + activate_url
                email = EmailMessage(
                    'JDM',
                    email_body,
                    'jdmrent2022@gmail.com',
                    [user.email],
                )
                email.send(fail_silently=False)
                messages.success(request, f'Your account has been successfully created.')
                return redirect('/')
            else:
                return render(
                    request,
                    'user/register.html',
                    {
                        'form': form,
                        "City": results,
                        "username": request.POST['username'],
                        "first_name": request.POST['first_name'],
                        "last_name": request.POST['last_name'],
                        "email": request.POST['email'],
                        "phone": request.POST['phone'],
                        "idn": request.POST['idn'],
                        "address": request.POST['address'],
                        "city": request.POST['city'],
                        "birthday": request.POST['birthday'],
                        "city_id": int(request.POST['city']),
                    }
                )
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


@login_required
def update(request):
    results = City.objects.all
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        if u_form.is_valid():
            u_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('user:profil')
    else:
        u_form = UserUpdateForm(instance=request.user)
    context = {
        'u_form': u_form,
        "City": results,
    }
    return render(request, 'user/profil.html', context)


def verify_email(request, token):
    if request.method == 'GET':
        try:
            user = CustomUser.objects.get(email_token=token)
            user.password_token = None
            user.email_verified = True
            user.is_active = True
            user.save()
            messages.success(request, f'Account activated!')
            return redirect('user:login')
        except CustomUser.DoesNotExist:
            return redirect('home:index')


def reset_password(request, token):
    if request.method == 'POST':
        try:
            user = CustomUser.objects.get(password_token=token)
            user.password_token = None
            user.set_password(request.POST['password2'])
            user.save()
            messages.success(request, f'Password reset success!')
            return redirect('user:login')
        except CustomUser.DoesNotExist:
            return redirect('home:index')
    else:
        return render(request, 'user/resetpassword.html', {'token': token})


def password_reset(request):
    if request.method == 'POST':
        try:
            user = CustomUser.objects.get(email=request.POST['email'])
            user.password_token = uuid4()
            user.save()
            domain = get_current_site(request).domain
            activate_url = 'http://' + domain + '/user/reset-password/' + str(user.password_token)
            email_body = 'Welcome ' + user.username + ' reset link\n ' + activate_url
            email = EmailMessage(
                'JDM',
                email_body,
                'jdmrent2022@gmail.com',
                [user.email],
            )
            email.send(fail_silently=False)
            messages.success(request, f'reset password link sent in email.')
            return redirect('home:index')
        except CustomUser.DoesNotExist:
            return redirect('home:index')
    else:
        return render(request, 'user/emailforestpassword.html')
