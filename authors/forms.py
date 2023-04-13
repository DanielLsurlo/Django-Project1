from django import forms  # type: ignore
from django.contrib.auth.models import User  # type: ignore


def add_placeholder(field, placeholder_val):
    field.widget.attrs['placeholder'] = placeholder_val


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

        labels = {
            'username': 'Username:',
            'first_name': 'First name:',
            'last_name': 'Last name:',
            'email': 'E-mail:',
        }
        help_texts = {
            'email': 'The e-mail must be valid',
        }
        error_messages = {
            'username': {
                'required': 'This field does not be empty',
            }
        }
