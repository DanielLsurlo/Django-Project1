# type: ignore
import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from selenium.webdriver.common.by import By

from .base import AuthorsBaseTest


@pytest.mark.functional_test
class AuthorsLoginTest(AuthorsBaseTest):
    def test_user_valid_data_can_login_successfully(self):
        string_password = 'pass'
        user = User.objects.create_user(
            username='my_user', password=string_password)

        # User open the login page
        self.browser.get(self.live_server_url + reverse('authors:login'))

        # User sees the login form
        form = self.browser.find_element(
            By.CLASS_NAME,
            'main-form'
        )
        username_field = self.get_by_placeholder(form, 'Type your username')
        password_field = self.get_by_placeholder(form, 'Type your password')

        # User type password and username
        username_field.send_keys(user.username)
        password_field.send_keys(string_password)

        # User submit the form
        form.submit()

        # User sees the success login message username
        self.assertIn(
            f'You are Logged with {user.username}.',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )

    def test_login_create_raises_404_if_not_POST_method(self):
        self.browser.get(self.live_server_url +
                         reverse('authors:login_create'))

        self.assertIn(
            'Not Found',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )

    def test_Login_with_invalid_credentials_raises_error(self):
        string_password = 'pass'
        user = User.objects.create_user(
            username='my_user', password=string_password)

        # User open the login page
        self.browser.get(self.live_server_url + reverse('authors:login'))

        # User sees the login form
        form = self.browser.find_element(
            By.CLASS_NAME,
            'main-form'
        )
        username_field = self.get_by_placeholder(form, 'Type your username')
        password_field = self.get_by_placeholder(form, 'Type your password')

        # User type the username and the wrong password
        username_field.send_keys(user.username)
        password_field.send_keys(string_password + '1')

        # User submit the form
        form.submit()

        self.assertIn(
            'Invalid credentials',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )

    def test_form_login_is_invalid(self):
        self.browser.get(
            self.live_server_url + reverse('authors:login')
        )

        # User sees the login form
        form = self.browser.find_element(By.CLASS_NAME, 'main-form')

        # User type username and password with space
        username = self.get_by_placeholder(form, 'Type your username')
        password = self.get_by_placeholder(form, 'Type your password')
        username.send_keys(' ')
        password.send_keys(' ')

        # User submit the form
        form.submit()

        self.assertIn(
            'Invalid username or password',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )
