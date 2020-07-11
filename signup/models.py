from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField("メールアドレス")
    icon = models.ImageField("アイコン", upload_to="Media", blank=True, null=False)
