from allauth.account import app_settings
from allauth.account.forms import LoginForm
from allauth.utils import set_form_field_order
from django import forms
from django.contrib.auth.forms import UserCreationForm

from user.models import Account


class LoginForm(LoginForm):
    password = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'id': 'password', 'class': 'form-control', 'type': 'password',
                'name': 'password', 'required': True, 'placeholder': 'Пароль'
            }
        )
    )
    remember = forms.CharField(
        required=False, widget=forms.TextInput(
            attrs={
                'id': 'is_remember', 'class': 'form-check-input',
                'type': 'checkbox', 'name': 'is_remember'
            }
        )
    )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(LoginForm, self).__init__(*args, **kwargs)
        login_widget = forms.TextInput(attrs={
            'name': 'login', 'class': 'form-control', 'type': 'email',
            'placeholder': 'E-mail', 'required': True,
            'autofocus': 'autofocus',
            'onkeyup': 'this.value = this.value.toLowerCase();'
        })
        login_field = forms.EmailField(label="E-mail",
                                       widget=login_widget)

        self.fields["login"] = login_field
        set_form_field_order(self, ["login", "password", "remember"])
        if app_settings.SESSION_REMEMBER is not None:
            del self.fields['remember']


def login(self, *args, **kwargs):
    return super(LoginForm, self).login(*args, **kwargs)


class SignupForm(UserCreationForm):
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'id': 'first_name', 'class': 'form-control', 'type': 'text',
                'name': 'first_name', 'required': True, 'placeholder': 'Имя',
                'autocomplete': 'off', 'pattern': '^[A-Za-zА-Яа-я]+$'

            }
        )
    )
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'id': 'last_name', 'class': 'form-control', 'type': 'text',
                'name': 'last_name', 'required': True, 'placeholder': 'Фамилия',
                'autocomplete': 'off', 'pattern': '^[A-Za-zА-Яа-я]+$'
            }
        )
    )
    birthday = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'id': 'birthday', 'class': 'form-control', 'type': 'date',
                'name': 'birthday', 'required': True,
                'autocomplete': 'off'
            }
        )
    )
    email = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'id': 'email', 'class': 'form-control', 'type': 'email',
                'name': 'email', 'required': True, 'autocomplete': 'off',
                'placeholder': 'Адрес электронной почты',
                'onkeyup': 'this.value = this.value.toLowerCase();'
            }
        )
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'id': 'password1', 'class': 'form-control', 'type': 'password',
                'name': 'password1', 'required': True, 'placeholder': 'Пароль',
                'autocomplete': 'off', 'min_length': 8
            }
        )
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'id': 'password2', 'class': 'form-control', 'type': 'password',
                'name': 'password2', 'required': True, 'min_length': 8,
                'placeholder': 'Повторите пароль', 'autocomplete': 'off'
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
