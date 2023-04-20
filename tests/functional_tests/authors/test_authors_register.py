# type: ignore
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from .base import AuthorsBaseTest


class AuthorsRegisterTest(AuthorsBaseTest):
    def get_by_placeholder(self, web_element, placeholder):
        return web_element.find_element(
            By.XPATH,
            f'//input[@placeholder="{ placeholder }"]'
        )

    def fill_form_dummy_data(self, form):
        fields = form.find_elements(By.TAG_NAME, 'input')

        for field in fields:
            if field.is_displayed():
                field.send_keys(' ' * 20)

    def get_browser_form(self):
        return self.browser.find_element(
            By.XPATH,
            '/html/body/main/div[2]/form'
        )

    def form_field_test_with_callback(self, callback):
        self.browser.get(self.live_server_url + '/authors/register/')
        form = self.get_browser_form()

        self.fill_form_dummy_data(form)
        form.find_element(By.NAME, 'email').send_keys('email@email.com')

        callback(form)
        return form

    def test_empty_first_name_error_message(self):
        def callback(form):
            first_name_field = self.get_by_placeholder(form, 'Ex.: Joe')
            first_name_field.send_keys(' ')
            first_name_field.send_keys(Keys.ENTER)

            form = self.get_browser_form()
            self.assertIn('Write your first name.', form.text)
        self.form_field_test_with_callback(callback)

    def test_empty_last_name_error_message(self):
        def callback(form):
            last_name_field = self.get_by_placeholder(form, 'Ex.: Souza')
            last_name_field.send_keys(' ')
            last_name_field.send_keys(Keys.ENTER)

            form = self.get_browser_form()
            self.assertIn('Write your last name.', form.text)
        self.form_field_test_with_callback(callback)

    def test_empty_username_error_message(self):
        def callback(form):
            username_field = self.get_by_placeholder(form, 'Your username')
            username_field.send_keys(' ')
            username_field.send_keys(Keys.ENTER)

            form = self.get_browser_form()
            self.assertIn('This field must not be empty', form.text)
        self.form_field_test_with_callback(callback)

    def test_invalid_email_error_message(self):
        def callback(form):
            email_field = self.get_by_placeholder(form, 'Your E-mail')
            email_field.send_keys('email@invalid')
            email_field.send_keys(Keys.ENTER)

            form = self.get_browser_form()
            self.assertIn('The e-mail must be valid', form.text)
        self.form_field_test_with_callback(callback)

    def test_invalid_password_error_message(self):
        def callback(form):
            password_field = self.get_by_placeholder(form, 'Your password')
            password_field.send_keys(' ')
            password_field.send_keys(Keys.ENTER)

            form = self.get_browser_form()
            self.assertIn('Follow the instructions.', form.text)
        self.form_field_test_with_callback(callback)

    def test_passwords_dont_match_error_message(self):
        def callback(form):
            password1_field = self.get_by_placeholder(form, 'Your password')
            password2_field = self.get_by_placeholder(
                form, 'Repeat your password')
            password1_field.send_keys('P@ssword')
            password2_field.send_keys('P@ssword2')
            password2_field.send_keys(Keys.ENTER)

            form = self.get_browser_form()
            self.assertIn('Passwords must be equal.', form.text)
        self.form_field_test_with_callback(callback)

    def test_valid_user_data_register_successfully(self):
        self.browser.get(self.live_server_url + '/authors/register/')
        form = self.get_browser_form()

        self.get_by_placeholder(form, 'Ex.: Joe').send_keys('First Name')
        self.get_by_placeholder(form, 'Ex.: Souza').send_keys('Last Name')
        self.get_by_placeholder(form, 'Your username').send_keys('First_Name')
        self.get_by_placeholder(
            form, 'Your E-mail').send_keys('email@email.com')
        self.get_by_placeholder(form, 'Your password').send_keys('P@ssword1')
        self.get_by_placeholder(
            form, 'Repeat your password').send_keys('P@ssword1')

        form.submit()

        self.assertIn(
            'Your user is Created, please log in.',
            self.browser.find_element(
                By.TAG_NAME,
                'body'
            ).text
        )
