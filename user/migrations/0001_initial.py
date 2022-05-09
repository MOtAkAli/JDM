# Generated by Django 4.0.4 on 2022-05-08 21:22

import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import user.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cities_light', '0011_alter_city_country_alter_city_id_alter_city_region_and_more'),
        ('auth', '0012_alter_user_first_name_max_length'),
        ('employee', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[(user.models.RoleEnum['CLIENT'], 'Client'), (user.models.RoleEnum['CLIENT_MANAGER'], 'ClientManager'), (user.models.RoleEnum['RESERVATION_MANAGER'], 'ReservationManager'), (user.models.RoleEnum['VEHICLE_MANAGER'], 'VehicleManager')], max_length=2, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('first_name', models.CharField(max_length=150)),
                ('last_name', models.CharField(max_length=150)),
                ('is_active', models.BooleanField(default=False)),
                ('inactive_reason', models.CharField(default='Email need to be verified', max_length=200)),
                ('idn', models.CharField(max_length=8)),
                ('birthday', models.DateField(null=True)),
                ('phone', models.CharField(max_length=15)),
                ('picture', models.ImageField(default='avatars/default.png', upload_to='avatars/')),
                ('address', models.CharField(max_length=200)),
                ('agency', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='employee.agency')),
                ('city', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='cities_light.city')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('roles', models.ManyToManyField(default='C', to='user.role')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
        ),
    ]
