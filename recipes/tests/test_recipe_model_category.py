from django.core.exceptions import ValidationError  # type: ignore

from .test_recipe_base import RecipeTestBase


class RecipeCategoryModelTest(RecipeTestBase):

    # setUp will be executed before the methods, everytime.
    # Must be carefully with waste of resources.
    def setUp(self) -> None:
        self.category = self.make_category(
            name='Category Testing'
        )
        return super().setUp()

    def test_recipe_categoy_model_string_representation_is_name_field(self):
        self.assertEqual(
            str(self.category),
            self.category.name
        )

    def test_recipe_categoy_model_name_max_length_is_65_chars(self):
        self.category.name = 'A'*66
        with self.assertRaises(ValidationError):
            self.category.full_clean()
