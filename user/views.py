from datetime import timedelta
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import UserRegisterForm, UserUpdateForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.contrib.auth import login as auth_login
from cities_light.models import City
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from user.models import CustomUser, RoleEnum, Role
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.utils import timezone

from uuid import uuid4

User = get_user_model()


def get_custom_user_roles(id):
    roles = {
        'is_client_manager': False,
        'is_reservation_manager': False,
        'is_vehicle_manager': False,
    }
    for role in CustomUser.objects.get(id=id).roles.values_list():
        if role[1] == RoleEnum.CLIENT_MANAGER.value:
            roles['is_client_manager'] = True
            continue
        if role[1] == RoleEnum.RESERVATION_MANAGER.value:
            roles['is_reservation_manager'] = True
            continue
        if role[1] == RoleEnum.VEHICLE_MANAGER.value:
            roles['is_vehicle_manager'] = True
    return roles


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
                user.roles.add(Role.objects.get(name=RoleEnum.CLIENT.value))
                domain = get_current_site(request).domain
                activate_url = request.scheme + '://' + domain + '/user/email-verification/' + str(user.email_token)
                email_body = render_to_string('user/email.html', {'activate_url': activate_url})
                message = EmailMultiAlternatives(
                    subject='Account Verification',
                    body='Use this link to verify your account ' + activate_url,
                    from_email=settings.EMAIL_HOST_USER,
                    to=(user.email,)
                )
                message.attach_alternative(email_body, "text/html")
                message.send(fail_silently=False)
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
            user_roles = get_custom_user_roles(user.id)
            if user.is_superuser:
                return redirect('/admin/')
            if user_roles['is_client_manager'] or user_roles['is_reservation_manager'] or user_roles['is_vehicle_manager']:
                return redirect('/employee/')
            messages.success(self.request, f'You are now logged in as {user.username}')
            return redirect('/')


@login_required
def update(request):
    results = City.objects.all
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        if u_form.is_valid():
            u_form.save()
            user_roles = get_custom_user_roles(request.user.id)
            if user_roles['is_client_manager'] or user_roles['is_reservation_manager'] or user_roles['is_vehicle_manager']:
                return redirect('/employee/')
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
            user.email_token = None
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
            if timezone.now() <= user.password_token_expiration:
                user.password_token = None
                user.password_token_expiration = None
                user.set_password(request.POST['password2'])
                user.save()
                messages.success(request, f'Password reset success!')
            else:
                messages.error(request, f'Link expired!')
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
            user.password_token_expiration = timezone.now() + timedelta(minutes=15)
            user.save()
            domain = get_current_site(request).domain
            activate_url = request.scheme + '://' + domain + '/user/reset-password/' + str(user.password_token)
            email_body = 'Welcome ' + user.username + ' reset link will expires after 15 min\n ' + activate_url
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
