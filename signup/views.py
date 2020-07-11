from django.shortcuts import render, redirect


from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib import messages

from django.views.generic import FormView, TemplateView, UpdateView
from django.views import View

from django.urls import reverse_lazy

from signup.models import User
from signup.forms import CustomUserCreationForm, CustomUserChangeForm, CustomUpdateForm


#アクセス制限（ログアウトしているユーザーのみ閲覧可能にする（会員登録、ログインページ）
class LogoutRequiredMixin(View):

    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect("eat:index")
        return super().dispatch(*args, **kwargs)

#アクセス制限（自身のページのみアクセス可能にする）　URLでの直接アクセス防止
class OnlyMixin(UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        user = self.request.user
        return user.pk == self.kwargs['pk'] or user.is_superuser

#会員登録ページ
class SignupCreateView(LogoutRequiredMixin, FormView):
    form_class = CustomUserCreationForm
    template_name = "signup/signup_new.html"
    success_url = reverse_lazy("signup:login")

    def form_valid(self, form):
        button = self.request.POST.get("next")
        if button == "back":
            return render(self.request, "signup/signup_new.html", {"form":form})
        elif button == "confirm":
            return render(self.request, "signup/signup_regist.html", {"form":form})
        elif button == "regist":
            form.save()
            messages.success(self.request, "会員登録が完了しました。ユーザー名とパスワードを入力してログインしてください")
            return super().form_valid(form)
        else:
            return redirect("signup:login")
        return super().form_valid(form)


class SignupLoginView(LogoutRequiredMixin, LoginView):
    template_name = "login.html"

    def form_valid(self, form):
        messages.success(self.request, "ログインしました")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "ログインできませんでした。正しいパスワードとユーザー名を入力してください")
        return super().form_invalid(form)


class SignupDetailView(LoginRequiredMixin, TemplateView):
    template_name = "signup/signup_detail.html"
    login_url = "/signup/login/"


class SignupUpdateView(LoginRequiredMixin, OnlyMixin, UpdateView):
    model = User
    form_class = CustomUserChangeForm
    template_name = "signup/signup_update.html"
    success_url = reverse_lazy("eat:index")
    login_url = "/signup/login/"

    def form_valid(self, form):
        messages.success(self.request, "ユーザー情報を変更しました")
        return super().form_valid(form)


class SignupPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    form_class = PasswordChangeForm
    template_name = "signup/signup_PasswordChange.html"
    success_url = reverse_lazy("eat:index")
    login_url = "/signup/login/"

    def form_valid(self, form):
        messages.success(self.request, "パスワードを変更しました")
        return super().form_valid(form)


class SignupDeleteView(LoginRequiredMixin, OnlyMixin, FormView):
    model = User
    form_class = CustomUpdateForm
    template_name = "signup/signup_delete.html"
    success_url = reverse_lazy("signup:new")
    login_url = "/signup/login/"

    def form_valid(self, form):
        self.request.user.is_active = False
        self.request.user.save()
        messages.success(self.request, "退会しました。再度アプリを利用するには会員登録が必要です")
        return super().form_valid(form)
