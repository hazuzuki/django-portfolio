from django.db import models
from signup.models import User
from django.conf import settings

class Recipe(models.Model):
    recipe_name = models.CharField("レシピ名", max_length=20)
    site = models.CharField("参考サイト", max_length=2048, blank=True, null=False)
    memo = models.TextField("メモ", max_length=1000, blank=True, null=False)
    photo = models.ImageField("写真", upload_to="Media", blank=True, null=False)
    ingredient = models.CharField("材料", max_length=200)
    TYPE = (
            ("スープ", "スープ"),
            ("ご飯", "ご飯"),
            ("おかず", "おかず"),
            ("スイーツ", "スイーツ")
            )
    type = models.CharField("種類", max_length=20, choices=TYPE)
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.recipe_name

    def summary(self):
        return self.site[:20]
