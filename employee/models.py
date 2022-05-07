from django.db import models
from django.utils import timezone
from user.models import CustomUser
from cities_light.models import City


class Agency(models.Model):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, unique=True)
    address = models.CharField(max_length=200)
    city = models.ForeignKey(City, on_delete=models.PROTECT)

    def __str__(self):
        return str(self.id) + " " + self.city.name


class EmployeeLog(models.Model):
    description = models.CharField(max_length=500)
    date_time = models.DateTimeField(default=timezone.now)
    employee = models.ForeignKey(CustomUser, on_delete=models.PROTECT)


class CarBrand(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class CarType(models.Model):
    CAR_TYPES = (
        ('SUV', 'Sports Utility Vehicle'),
        ('H', 'Hatchback'),
        ('CO', 'Crossover'),
        ('CI', 'Convertible'),
        ('S', 'Sedan'),
        ('SC', 'Sports Car'),
        ('CP', 'Coupe'),
        ('M', 'Minivan'),
        ('SW', 'Station Wagon'),
        ('PT', 'Pickup Truck'),
    )
    name = models.CharField(max_length=3, choices=CAR_TYPES, unique=True)

    def __str__(self):
        return self.name


class CarModel(models.Model):
    name = models.CharField(max_length=150, unique=True)
    carModelPrice = models.FloatField()
    carBrand = models.ForeignKey(CarBrand, on_delete=models.PROTECT)

    def __str__(self):
        return self.carBrand.name + " " + self.name


class Car(models.Model):
    GEARBOXES = (
        ('AMT', 'Automated Manual Transmission'),
        ('CVT', 'Continuous Variable Transmission'),
        ('DCT', 'Dual Clutch Transmission'),
        ('TC', 'Torque Converters'),
        ('IMT', 'Intelligent Manual Transmission'),
    )
    FUELS = (
        ('G', 'Gasoline'),
        ('D', 'Diesel'),
        ('BD', 'Bio Diesel'),
        ('E', 'Ethanol'),
    )
    doors = models.PositiveSmallIntegerField()
    seats = models.PositiveSmallIntegerField()
    ac = models.BooleanField()
    gearbox = models.CharField(max_length=3, choices=GEARBOXES)
    fuel = models.CharField(max_length=2, choices=FUELS)
    year = models.PositiveSmallIntegerField()
    picture = models.ImageField(upload_to='cars/', default='cars/default.png')
    carType = models.ForeignKey(CarType, on_delete=models.PROTECT)
    carModel = models.ForeignKey(CarModel, on_delete=models.PROTECT)
    agency = models.ForeignKey(Agency, on_delete=models.PROTECT)

    def __str__(self):
        return self.carType.name + " " + str(self.carModel)


class Reservation(models.Model):
    startDate = models.DateField()
    endDate = models.DateField()
    price = models.FloatField()
    car = models.ForeignKey(Car, on_delete=models.PROTECT)
    client = models.ForeignKey(CustomUser, related_name='client', on_delete=models.PROTECT)
    employee = models.ForeignKey(CustomUser, related_name='employee', on_delete=models.PROTECT, null=True)
