from django.contrib import admin
from .models import CustomUser, Role

admin.site.register(CustomUser)
admin.site.register(Role)
