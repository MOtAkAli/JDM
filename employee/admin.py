from django.contrib import admin
from .models import Employee, EmployeeLog, CarBrand, CarType, CarModel, Agency, Car, Reservation, City

admin.site.register(City)
admin.site.register(Employee)
admin.site.register(EmployeeLog)
admin.site.register(CarBrand)
admin.site.register(CarModel)
admin.site.register(CarType)
admin.site.register(Agency)
admin.site.register(Car)
admin.site.register(Reservation)
