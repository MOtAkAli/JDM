from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = 'user'

urlpatterns = [
    path("register/", views.register, name="register"),
    path('logout/', auth_views.LogoutView.as_view(template_name='home/index.html'), name='logout'),
    path('login/', views.LoginView.as_view(redirect_authenticated_user=True), name='login'),
]
