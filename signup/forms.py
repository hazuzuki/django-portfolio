from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ("username", "email")

class CustomUserChangeForm(UserChangeForm):
    password = None

    class Meta:
        model = User
        fields = ("username", "icon", "email")


    # 入力後戻った時にパスワードも入力済みにする　
class CustomUpdateForm(UserChangeForm):

    class Meta:
        model = User
        fields = ['is_active']
