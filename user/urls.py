from django.urls import path
from .views import register_view, update_view, login_view, logout_view, verify_email_view, password_reset_view, \
    reset_password_view

app_name = 'user'

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name="register"),
    path('profil/', update_view, name="profil"),
    path('email_verification/<uidb64>/<token>/', verify_email_view, name='verify_email'),
    path('password_reset/', password_reset_view, name='password_reset'),
    path('reset_password/<uidb64>/<token>/', reset_password_view, name='reset_password'),
]
