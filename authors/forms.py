from django import forms  # type: ignore
from django.contrib.auth.models import User  # type: ignore


class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',

        ]
