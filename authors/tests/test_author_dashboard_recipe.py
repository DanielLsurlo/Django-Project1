# type: ignore
# from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import resolve, reverse

from authors import views
from recipes.tests.test_recipe_base import RecipeTestBase


class AuthorDashboardTest(RecipeTestBase):
    def test_authors_dashboard_views_function_is_correct(self):
        view = resolve(
            reverse('authors:dashboard_recipe_new'))
        self.assertIs(view.func.view_class, views.DashboardRecipe)

    def test_authors_dashboard_view_returns_status_code_200_OK(self):
        User.objects.create_user(username='my_user', password='my_pass')
        self.client.login(username='my_user', password='my_pass')

        response = self.client.get(reverse('authors:dashboard_recipe_new'))
        self.assertEqual(response.status_code, 200)
