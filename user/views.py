from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from .forms import UserRegisterForm,UserUpdateForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.contrib.auth import login as auth_login
from cities_light.models import City
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes,force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from .utils import account_activation_token

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
                username = form.cleaned_data.get('username')
                user.save()
                uid64 = urlsafe_base64_encode(force_bytes(user.pk))
                domain = get_current_site(request).domain
                link = reverse('activate',kwargs={'uid64': uid64, 'token': account_activation_token.make_token(user)})
                activate_url = 'http://' + domain + link
                email_body = 'Welcome ' + user.username + ' Please verify your account\n ' + activate_url
                email = EmailMessage(
                    'JDM',
                    email_body,
                    'jdmrent2022@gmail.com',
                    [user.email],
                )
                email.send(fail_silently=False)
                messages.success(request, f'Your account has been successfully created.Check your mail')
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
        if request.method == 'POST':
            print("dkhl if post")
            u_form = UserUpdateForm(request.POST, instance=request.user)
            if u_form.is_valid() :
                print("dkhl if form is valid")
                u_form.save()
                messages.success(request, f'Your account has been updated!')
                return redirect('home:index')
            print("form not valid")
        else:
            u_form = UserUpdateForm(instance=request.user)


        context = {
            'u_form': u_form,
        }

        return render(request, 'user/profil.html', context)


class VerificationView(View):
    def get(self, request, uidb64, token):
        try:
            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)

            if not account_activation_token.check_token(user, token):
                return redirect('login'+'?message='+'User already activated')

            if user.is_active:
                return redirect('user:login')
            user.is_active = True
            user.save()

            messages.success(request, 'Account activated successfully')
            return redirect('login')

        except Exception as ex:
            pass

        return redirect('user:login')
