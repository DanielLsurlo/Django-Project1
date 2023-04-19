# type: ignore

import pytest
from selenium.webdriver.common.by import By

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

    def test_recipe_home_page_without_recipes_not_found_message(self):
        self.browser.get(self.live_server_url)
        body = self.browser.find_element(By.TAG_NAME, 'body')
        self.assertIn('No recipes found here.', body.text)
