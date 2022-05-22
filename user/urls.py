from django.urls import path
from django.contrib.auth import views as auth_views

from . import views
from .views import VerificationView

app_name = 'user'

urlpatterns = [
    path('register/', views.register, name="register"),
    path('profil/', views.update, name="profil"),
    path('logout/', auth_views.LogoutView.as_view(template_name='home/index.html'), name='logout'),
    path('login/', views.LoginView.as_view(redirect_authenticated_user=True), name='login'),
    path('activate/<uid64>/<token>', VerificationView.as_view(), name='activate'),
]
