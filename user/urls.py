from django.urls import path
from django.contrib.auth import views as auth_views

from . import views
from .views import verify_email, reset_password, password_reset

app_name = 'user'

urlpatterns = [
    path('register/', views.register, name="register"),
    path('profil/', views.update, name="profil"),
    path('logout/', auth_views.LogoutView.as_view(template_name='home/index.html'), name='logout'),
    path('login/', views.LoginView.as_view(redirect_authenticated_user=True), name='login'),
    path('reset-password/<uuid:token>', reset_password, name='reset_password'),
    path('password-reset', password_reset, name='password_reset'),
    path('email-verification/<uuid:token>', verify_email, name='verify_email'),
]
