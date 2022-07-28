from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.urls import reverse
from .forms import UserRegistrationForm, UserResetPasswordForm, UserUpdateForm
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib import messages
from cities_light.models import City
from django.contrib.sites.shortcuts import get_current_site
from user.models import CustomUser, RoleEnum, Role
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.core.validators import validate_email
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .utils import EmailVerificationTokenGenerator

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


def send_email_verification(request, user):
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    token = EmailVerificationTokenGenerator().make_token(user)
    domain = get_current_site(request).domain
    activate_url = request.scheme + '://' + domain + reverse('user:verify_email', args=(uidb64, token))
    email_template = render_to_string('user/email_verification_email.html', {'activate_url': activate_url})
    email = EmailMultiAlternatives(
        subject='Account Verification',
        body='Use this link to verify your account email ' + activate_url,
        from_email=settings.EMAIL_HOST_USER,
        to=(user.email,)
    )
    email.attach_alternative(email_template, "text/html")
    email.send(fail_silently=False)


def register_view(request):
    if request.user.is_authenticated:
        messages.info(request, 'Your are already logged in.')
        return render(request, 'home/index.html')

    cities = City.objects.all()

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            user.roles.add(Role.objects.get(name=RoleEnum.CLIENT.value))
            send_email_verification(request, user)
            messages.success(request, 'Your account has been successfully created check your email.')
            return redirect('home:index')
        else:
            return render(
                request,
                'user/register.html',
                {
                    'form': form,
                    'cities': cities,
                    'username': request.POST.get('username'),
                    'first_name': request.POST.get('first_name'),
                    'last_name': request.POST.get('last_name'),
                    'idn': request.POST.get('idn'),
                    'birthday': request.POST.get('birthday'),
                    'phone': request.POST.get('phone'),
                    'address': request.POST.get('address'),
                    'city_id': int(request.POST.get('city')),
                    'email': request.POST.get('email'),
                }
            )
    return render(request, 'user/register.html', {'cities': cities})


def login_view(request):
    if request.user.is_authenticated:
        messages.success(request, 'You already logged in.')
        return redirect("home:index")
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if not username or not password:
            return render(request, 'user/login.html', {
                'error_message': 'Username and Password are required.',
            })
        user = authenticate(request, username=username, password=password)
        if user is None:
            return render(request, 'user/login.html', {
                'error_message': 'Your username or password is invalid.',
            })
        # if email is not verified
        if not user.email_verified:
            send_email_verification(request, user)
            return render(request, 'user/login.html', {
                'error_message': 'Check your email for verification.',
            })
        if not user.is_active:
            return render(request, 'user/login.html', {
                'error_message': 'Your account is deactivated contact administration.',
            })
        login(request, user)
        user_roles = get_custom_user_roles(user.id)
        if user.is_superuser:
            return redirect('admin:index')
        if user_roles['is_client_manager'] or user_roles['is_reservation_manager'] or user_roles['is_vehicle_manager']:
            return redirect('employee:index')
        messages.success(request, 'Successful login.')
        return redirect('home:index')
    return render(request, 'user/login.html')


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request, 'Successful logout')
        return redirect('home:index')

    messages.error(request, 'Unsuccessful logout')
    return redirect('home:index')


@login_required
def update_view(request):
    results = City.objects.all
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        if u_form.is_valid():
            u_form.save()
            user_roles = get_custom_user_roles(request.user.id)
            if user_roles['is_client_manager'] or user_roles['is_reservation_manager'] or user_roles[
                'is_vehicle_manager']:
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


def verify_email_view(request, uidb64, token):
    try:
        user_pk = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=user_pk)
        try:
            if not EmailVerificationTokenGenerator().check_token(user, token):
                raise ValidationError(message='Invalid token')
        except ValidationError:
            return render(request, 'user/email_verification_error.html')
        user.email_verified = True
        user.is_active = True
        user.save()
        messages.success(request, 'Email verification done.')
        return redirect('user:login')
    except ValueError or CustomUser.DoesNotExist:
        return render(request, 'user/email_verification_error.html')


def reset_password_view(request, uidb64, token):
    try:
        user_pk = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=user_pk)
        try:
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise ValidationError(message='Invalid token')
        except ValidationError:
            return render(request, 'user/password_reset_error.html')
        if request.method == 'POST':
            form = UserResetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Reset password success')
                return redirect('user:login')
            else:
                return render(request, 'user/reset_password.html', {
                    'form': form,
                })
        return render(request, 'user/reset_password.html')
    except ValueError or CustomUser.DoesNotExist:
        return render(request, 'user/password_reset_error.html')


def password_reset_view(request):
    if request.method == 'POST':
        try:
            email = request.POST['email']
            validate_email(email)
            user = CustomUser.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            token = PasswordResetTokenGenerator().make_token(user)
            domain = get_current_site(request).domain
            password_reset_url = request.scheme + '://' + domain + reverse('user:reset_password', args=(uidb64, token))
            email_template = render_to_string('user/password_reset_email.html', {
                'username': user.username,
                'password_reset_url': password_reset_url,
            })
            email = EmailMultiAlternatives(
                subject='Password Reset',
                body=f'Hey {user.username} you have requested a password reset.'
                     f'Be aware that the link will expire after 20 min.'
                     f'{password_reset_url}',
                from_email=settings.EMAIL_HOST_USER,
                to=(user.email,),
            )
            email.attach_alternative(email_template, "text/html")
            email.send(fail_silently=False)
            return render(request, 'user/password_reset_done.html')
        except ValidationError:
            messages.error(request, 'Enter valid email address')
            return redirect('user:password_reset')
        except CustomUser.DoesNotExist:
            messages.error(request, 'Provided email address did not match any user')
            return redirect('user:password_reset')

    return render(request, 'user/password_reset.html')
