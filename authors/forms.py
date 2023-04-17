import re

from django import forms  # type: ignore
from django.contrib.auth.models import User  # type: ignore
from django.core.exceptions import ValidationError  # type: ignore


def add_placeholder(field, placeholder_val):
    field.widget.attrs['placeholder'] = placeholder_val


def strong_password(password):
    regex = re.compile(r'(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$')

    if not regex.match(password):
        raise ValidationError((
            'Password must have at least one uppercase letter, '
            'one lowercase letter and one number. The length should be '
            'at least 8 characters.'
        ),
            code='invalid',
        )


class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['username'], 'Your username')
        add_placeholder(self.fields['email'], 'Your E-mail')
        add_placeholder(self.fields['first_name'], 'Ex.: Joe')
        add_placeholder(self.fields['last_name'], 'Ex.: Souza')
        add_placeholder(self.fields['password'], 'Your password')
        add_placeholder(self.fields['password2'], 'Repeat your password')

    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(),
        label='Confirm password:',
        error_messages={
            'required': 'Repeat the password.'
        },
    )

    password = forms.CharField(
        required=True,
        error_messages={
            'required': 'Follow the instructions.'
        },
        help_text=(
            'Password must have at least one uppercase letter, '
            'one lowercase letter and one number. The length should be '
            'at least 8 characters.'
        ),
        label='Password:',
        widget=forms.PasswordInput(),
        validators=[strong_password],

    )

    email = forms.EmailField(
        required=True,
        help_text=(
            'The e-mail must be valid'
        ),
        label='E-mail:',
        error_messages={
            'required': 'This field is required'
        },
    )

    first_name = forms.CharField(
        error_messages={'required': 'Write your first name.'},
        required=True,
        label='First name:',
    )

    last_name = forms.CharField(
        error_messages={'required': 'Write your last name.'},
        required=True,
        label='Last name:',
    )

    username = forms.CharField(
        label='Username:',
        error_messages={
            'required': 'This field must not be empty',
            'min_length': 'Username must have between 4 and 150 chars.',
            'max_length': 'Username must have between 4 and 150 chars.',
        },
        required=True,
        help_text=(
            'Username must have letters, numbers or special characters.'
            'The length should be between 4 and 150 characters.'
        ),
        min_length=4,
        max_length=150,
    )

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
        ]

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password != password2:
            password_confirm_error = ValidationError(
                'Passwords must be equal.',
                code='invalid'
            )
            raise ValidationError({
                'password': password_confirm_error,
                'password2': [
                    password_confirm_error,
                ],
            }
            )
