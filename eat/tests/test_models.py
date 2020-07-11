from django.test import TestCase

from eat.models import Recipe
from signup.models import User

class RecipeModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user("sample_name", "sample@gmail.com", "pass")
        Recipe.objects.create(
            recipe_name="sample",
            site="sample.url",
            memo="sample",
            photo="sample.img",
            ingredient="sample",
            type="ご飯",
            date="2018-10-25 14:30:59",
            user=user,
            )

    def test_recipe_name_label(self):
        recipe = Recipe.objects.get(id=1)
        field_label = recipe._meta.get_field("recipe_name").verbose_name
        self.assertEqual(field_label, "レシピ名")

    def test_site_label(self):
        recipe = Recipe.objects.get(id=1)
        object_label = recipe._meta.get_field("site").verbose_name
        self.assertEqual(object_label, "参考サイト")

    def test_memo_label(self):
        recipe = Recipe.objects.get(id=1)
        object_label = recipe._meta.get_field("memo").verbose_name
        self.assertEqual(object_label, "メモ")

    def test_photo_label(self):
        recipe = Recipe.objects.get(id=1)
        object_label = recipe._meta.get_field("photo").verbose_name
        self.assertEqual(object_label, "写真")

    def test_ingredient_label(self):
        recipe = Recipe.objects.get(id=1)
        object_label = recipe._meta.get_field("ingredient").verbose_name
        self.assertEqual(object_label, "材料")

    def test_tyle_label(self):
        recipe = Recipe.objects.get(id=1)
        object_label = recipe._meta.get_field("type").verbose_name
        self.assertEqual(object_label, "種類")

    def test_recipe_name_max_length(self):
        recipe = Recipe.objects.get(id=1)
        max_length = recipe._meta.get_field("recipe_name").max_length
        self.assertEqual(max_length, 20)

    def test_site_max_length(self):
        recipe = Recipe.objects.get(id=1)
        max_length = recipe._meta.get_field("site").max_length
        self.assertEqual(max_length, 2048)

    def test_memo_max_length(self):
        recipe = Recipe.objects.get(id=1)
        max_length = recipe._meta.get_field("memo").max_length
        self.assertEqual(max_length, 1000)

    def test_ingredient_max_length(self):
        recipe = Recipe.objects.get(id=1)
        max_length = recipe._meta.get_field("ingredient").max_length
        self.assertEqual(max_length, 200)

    def test_type_max_length(self):
        recipe = Recipe.objects.get(id=1)
        max_length = recipe._meta.get_field("type").max_length
        self.assertEqual(max_length, 20)

    def test_image_upload(self):
        recipe = Recipe.objects.get(id=1)
        upload_to = recipe._meta.get_field("photo").upload_to
        self.assertEqual(upload_to, "Media")

    def test_str(self):
        recipe = Recipe.objects.get(id=1)
        self.assertEqual(recipe.recipe_name, "sample")
