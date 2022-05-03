from django.forms import ModelForm
from user.models import User


class ClientForm(ModelForm):
    class Meta:
        model = User
        fields = ['idn', 'firstname', 'lastname', 'birthday', 'phone', 'email', 'password','picture', 'address', 'city']
