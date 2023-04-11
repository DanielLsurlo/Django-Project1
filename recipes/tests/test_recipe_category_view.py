from unittest.mock import patch

from django.urls import resolve, reverse  # type: ignore

from recipes import views

from .test_recipe_base import RecipeTestBase


class RecipeCategoryViewTest(RecipeTestBase):
    def test_recipe_category_views_function_is_correct(self):
        view = resolve(
            reverse('recipes:category', kwargs={'category_id': 1000}))
        self.assertIs(view.func, views.category)

    def test_recipe_category_view_returns_404_if_no_recipes_found(self):
        response = self.client.get(
            reverse('recipes:category', kwargs={'category_id': 1000}))
        self.assertEqual(response.status_code, 404)

    def test_recipe_category_template_loads_recipes(self):
        needed_title = 'this is a category test'
        # Need a recipe for this test
        self.make_recipe(title=needed_title)

        response = self.client.get(reverse('recipes:category', args=(1,)))
        content = response.content.decode('utf-8')

        # Check if one recipe exists
        self.assertIn(needed_title, content)

    def test_recipe_category_template_dont_load_recipes_not_published(self):
        """Test recipe is_published False dont show."""

        # Need a recipe for this test
        recipe = self.make_recipe(is_published=False)

        response = self.client.get(reverse(
            'recipes:recipe', kwargs={'id': recipe.category.id}))

        self.assertEqual(response.status_code, 404)

    def test_recipe_category_is_paginated(self):
        category_test = self.make_category()
        for i in range(6):
            kwargs = {'author_data': {'username': f'u{i}'},
                      'slug': f'r{i}', }
            self.make_recipe_with_same_category(
                category_data=category_test, **kwargs)

        with patch('recipes.views.PER_PAGE', new=2):
            response = self.client.get(
                reverse('recipes:category',
                        kwargs={'category_id': 1}))
            recipes = response.context['recipes']
            paginator = recipes.paginator

        self.assertEqual(paginator.num_pages, 3)
        self.assertEqual(len(paginator.get_page(1)), 2)
        self.assertEqual(len(paginator.get_page(2)), 2)
        self.assertEqual(len(paginator.get_page(3)), 2)
