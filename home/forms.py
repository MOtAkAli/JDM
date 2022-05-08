from django.forms import ModelForm
from user.models import CustomUser


class ClientForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = ['idn', 'first_name', 'last_name', 'birthday', 'phone', 'email', 'password', 'picture', 'address',
                  'city']