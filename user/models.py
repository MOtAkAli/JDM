from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from cities_light.models import City


class Role(models.Model):
    ROLES = (
        ('C', 'Client'),
        ('CM', 'ClientManager'),
        ('RM', 'ReservationManager'),
        ('VM', 'VehicleManager'),
    )
    name = models.CharField(max_length=2, choices=ROLES, unique=True)

    def __str__(self):
        return self.name


"""class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password, **other_fields):
        if not email:
            raise ValueError('You must provide valid email address')

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **other_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password, **other_fields):
        other_fields.setdefault('is_active', True)
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(username, email, password, **other_fields)"""


class CustomUser(AbstractUser):
    idn = models.CharField(max_length=8)
    birthday = models.DateField(null=True)
    phone = models.CharField(max_length=15)
    picture = models.ImageField(upload_to='avatars/', default='avatars/default.png')
    address = models.CharField(max_length=200)
    roles = models.ManyToManyField(Role, default='C')
    city = models.ForeignKey(City, blank=True, null=True, on_delete=models.PROTECT)
    agency = models.ForeignKey('employee.Agency', null=True, blank=True, on_delete=models.PROTECT)

    def __str__(self):
        return self.username
