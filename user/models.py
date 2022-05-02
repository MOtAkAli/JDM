from django.db import models


class User(models.Model):
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
    city = models.ForeignKey('employee.City', on_delete=models.PROTECT)

    def __str__(self):
        return self.nic + " " + self.firstname + " " + self.lastname
