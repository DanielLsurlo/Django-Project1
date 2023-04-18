from unittest import TestCase

from django.test import TestCase as DjangoTestCase  # type: ignore
from django.urls import reverse  # type: ignore
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
        ('username', (
            'Username must have letters, numbers or special characters.'
            'The length should be between 4 and 150 characters.'
        ))

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


class AuthorRegisterFormIntegrationTest(DjangoTestCase):
    def setUp(self, *args, **kwargs):
        self.form_data = {
            'username': 'user',
            'first_name': 'first',
            'last_name': 'last',
            'email': 'email@anyemail.com',
            'password': 'Str0nfP@ssword1',
            'password2': 'Str0nfP@ssword1',
        }
        return super().setUp(*args, **kwargs)

    @parameterized.expand([
        ('username', 'This field must not be empty'),
        ('first_name', 'Write your first name.'),
        ('last_name', 'Write your last name.'),
        ('password', 'Follow the instructions.'),
        ('password2', 'Repeat the password.'),
        ('email', 'This field is required'),
    ])
    def test_fields_cannot_be_empty(self, field, msg):
        self.form_data[field] = ''
        url = reverse('authors:create')

        # 'follow=True' to follow a url when a have a redirect in view.
        response = self.client.post(url, data=self.form_data, follow=True)

        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get(field))

    def test_username_field_min_length_should_be_4(self):
        self.form_data['username'] = 'joa'
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)

        msg = 'Username must have between 4 and 150 chars.'

        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get('username'))

    def test_username_field_max_length_should_be_150(self):
        self.form_data['username'] = 'A'*151
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)

        msg = 'Username must have between 4 and 150 chars.'

        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get('username'))

    def test_password_field_have_lower_upper_case_letter_and_numbers(self):
        self.form_data['password'] = 'abc123'
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)

        msg = ('Password must have at least one uppercase letter, '
               'one lowercase letter and one number. The length should be '
               'at least 8 characters.')

        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get('password'))

        self.form_data['password'] = '@Abc1234'
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)

        msg = ('Password must have at least one uppercase letter, '
               'one lowercase letter and one number. The length should be '
               'at least 8 characters.')

        self.assertNotIn(msg, response.context['form'].errors.get('password'))

    def test_password_and_password_confirmation_are_equal(self):
        self.form_data['password'] = '@Abc1234'
        self.form_data['password2'] = '@Abc12345'

        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)

        msg = ('Passwords must be equal.')

        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get('password'))

        self.form_data['password'] = '@Abc12345'
        self.form_data['password2'] = '@Abc12345'

        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)

        self.assertNotIn(msg, response.content.decode('utf-8'))

    def test_send_get_request_to_registration_create_view_returns_404(self):
        url = reverse('authors:create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
