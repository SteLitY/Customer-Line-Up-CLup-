from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomerSignUpForm(UserCreationForm):
    middle_name = forms.CharField(max_length=100, help_text='')
    cell_number = forms.CharField(max_length=12, help_text='')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'middle_name', 'last_name', 'password1', 'password2', 'email',  'cell_number')