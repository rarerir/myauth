from django.contrib.auth.admin import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import *
from django.utils.translation import gettext_lazy as _

class RegisterForm(UserCreationForm):
    email = EmailField(
        required=True,
        label="Email",
        widget= EmailInput(attrs={
            'autofocus': True,
            'placeholder': 'example@email.com',
            'class': 'form-control'
        })
    )

    username = CharField(
        required=True,
        label="Логин",
        widget= TextInput(attrs={
            'autofocus': True,
            'placeholder': 'Логин',
            'class': 'form-control'
        })
    )
    password1 = CharField(
        required=True,
        label=_("Password"),
        strip=False,
        widget= PasswordInput(attrs={
            "autocomplete": "new-password",
            'placeholder': 'Пароль',
            'class': 'form-control'
        }),
    )

    password2 = CharField(
        required=True,
        label=_("Password confirmation"),
        strip=False,
        widget= PasswordInput(attrs={
            "autocomplete": "new-password",
            'placeholder': 'Подтверждение пароля',
            'class': 'form-control'
        }),
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class LoginForm(Form):
    email = EmailField(
        label="Email",
        widget= EmailInput(attrs={
            'autofocus': True,
            "autocomplete": "email",
            'placeholder': 'example@email.com',
            'class': 'form-control'
        })
    )
    password = CharField(
        label=_("Password"),
        strip=False,
        widget=PasswordInput(attrs={
            "autocomplete": "current-password",
            'placeholder': 'Пароль',
            'class': 'form-control'
        }),

    )

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        if email and password:
            try:
                user = User.objects.get(email=email)
            except User.objects.DoesNotExist:
                raise ValidationError('Неверный email или пароль')
            if not user.check_password(password):
                raise ValidationError('Неверный email или пароль')
            self.user_cache = user
        return cleaned_data

    def get_user(self):
        return getattr(self, 'user_cache', None)