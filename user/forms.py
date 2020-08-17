from django import forms
from django.contrib.auth.forms import UserCreationForm

from user.models import Account


class SignupForm(UserCreationForm):
    email = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'id': 'email', 'class': 'validate', 'type': 'email',
                'name': 'email', 'required': True, 'autocomplete': 'off',
                'onkeyup': 'this.value = this.value.toLowerCase();'

            }
        )
    )
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'id': 'first_name', 'class': 'validate', 'type': 'text',
                'name': 'first_name', 'required': True,
                'autocomplete': 'off', 'pattern': '^[A-Za-zА-Яа-я]+$'

            }
        )
    )
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'id': 'last_name', 'class': 'validate', 'type': 'text',
                'name': 'last_name', 'required': True,
                'autocomplete': 'off', 'pattern': '^[A-Za-zА-Яа-я]+$'
            }
        )
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'id': 'password1', 'class': 'validate', 'type': 'password',
                'name': 'password1', 'required': True,
                'autocomplete': 'off', 'min_length': 8
            }
        )
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'id': 'password2', 'class': 'validate', 'type': 'password',
                'name': 'password2', 'required': True,
                'autocomplete': 'off', 'min_length': 8
            }
        )
    )

    class Meta:
        model = Account
        fields = (
            'first_name', 'last_name', 'birthday', 'email', 'password1',
            'password2'
        )
        exclude = ('url',)
