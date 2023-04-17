from django.test import TestCase  # type: ignore
from parameterized import parameterized  # type: ignore

from authors.forms import RegisterForm


class AuthorRegisterFormUnitTest(TestCase):
    @parameterized.expand([
        ('username', 'Your username'),
        ('email', 'Your E-mail'),
        ('first_name', 'Ex.: Joe'),
        ('last_name', 'Ex.: Souza'),
        ('password', 'Your password'),
        ('password2', 'Repeat your password'),
    ])
    def test_fields_placeholder_is_correct(self, field, placeholder):
        form = RegisterForm()
        current_placeholder = form[field].field.widget.attrs['placeholder']
        self.assertEqual(placeholder, current_placeholder)

    @parameterized.expand([
        ('password', (
            'Password must have at least one uppercase letter, '
            'one lowercase letter and one number. The length should be '
            'at least 8 characters.'
        )),
        ('email', 'The e-mail must be valid'),

    ])
    def test_fields_help_test_is_correct(self, field, needed):
        form = RegisterForm()
        current = form[field].field.help_text
        self.assertEqual(needed, current)

    @parameterized.expand([
        ('username', 'Username:'),
        ('email', 'E-mail:'),
        ('first_name', 'First name:'),
        ('last_name', 'Last name:'),
        ('password', 'Password:'),
        ('password2', 'Confirm password:'),
    ])
    def test_fields_label_is_correct(self, field, needed):
        form = RegisterForm()
        current = form[field].field.label
        self.assertEqual(needed, current)
