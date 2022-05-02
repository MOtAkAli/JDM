from django.db import models
from user.models import User


class City(models.Model):
    name = models.CharField(max_length=187)

    def __str__(self):
        return self.name


class Employee(models.Model):
    ROLES = (
        ('A', 'Admin'),
        ('R', 'Reservation'),
        ('C', 'Car'),
    )
    role = models.CharField(max_length=1, choices=ROLES)
    nic = models.CharField(max_length=8)
    firstname = models.CharField(max_length=64)
    lastname = models.CharField(max_length=64)
    birthday = models.DateField()
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    password = models.CharField(max_length=255)
    picture = models.CharField(max_length=260)
    active = models.BooleanField()
    address = models.CharField(max_length=200)
    city = models.ForeignKey(City, on_delete=models.PROTECT)

    def __str__(self):
        return self.nic + " " + self.firstname + " " + self.lastname


class EmployeeLog(models.Model):
    description = models.CharField(max_length=500)
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT)


class CarBrand(models.Model):
    name = models.CharField(max_length=100)

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
    name = models.CharField(max_length=3, choices=CAR_TYPES)

    def __str__(self):
        return self.name


class CarModel(models.Model):
    name = models.CharField(max_length=150)
    carModelPrice = models.FloatField()
    carBrand = models.ForeignKey(CarBrand, on_delete=models.PROTECT)

    def __str__(self):
        return self.carBrand.name + " " + self.name


class Agency(models.Model):
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=200)
    city = models.ForeignKey(City, on_delete=models.PROTECT)

    def __str__(self):
        return str(self.id) + " " + self.city.name


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
    carType = models.ForeignKey(CarType, on_delete=models.PROTECT)
    carModel = models.ForeignKey(CarModel, on_delete=models.PROTECT)
    agency = models.ForeignKey(Agency, on_delete=models.PROTECT)

    def __str__(self):
        return self.carType.name + " " + str(self.carModel)


class Reservation(models.Model):
    startDate = models.DateTimeField()
    endDate = models.DateTimeField()
    price = models.FloatField()
    car = models.ForeignKey(Car, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT)
