# type: ignore

from unittest.mock import patch

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from .base import RecipeBaseFunctionalTest

# from django.test import LiveServerTestCase
# it can run with the same porpose of StaticLiveServerTestCase, but it doesn't
# run static files.
# the performance is better.

# --headless is defined in .env doc, if you wannna see the page set it to 0

# run: pytest -m 'functional_test'
# or: pytest -m 'not functional_test'


@pytest.mark.functional_test
class RecipeHomePageFunctionalTest(RecipeBaseFunctionalTest):
    @patch('recipes.views.PER_PAGE', new=2)
    def test_recipe_home_page_without_recipes_not_found_message(self):
        self.browser.get(self.live_server_url)
        body = self.browser.find_element(By.TAG_NAME, 'body')
        self.assertIn('No recipes found here.', body.text)

    @patch('recipes.views.PER_PAGE', new=2)
    def test_recipe_search_input_can_find_correct_recipes(self):
        recipes = self.make_recipe_in_batch()

        title_needed = 'This is what I need'

        recipes[0].title = title_needed
        recipes[0].save()

        # User enter the page
        self.browser.get(self.live_server_url)

        # See a search field with the phase "Search for a recipe"
        search_input = self.browser.find_element(
            By.XPATH,
            '//input[@placeholder="Search for a recipe"]'
        )

        # Click on input, and type the search term,
        # to find this title with de title.
        search_input.send_keys(title_needed)
        search_input.send_keys(Keys.ENTER)

        self.assertIn(
            title_needed,
            self.browser.find_element(
                By.CLASS_NAME,
                'main-content-list'
            ).text
        )
