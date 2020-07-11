import os
from django.test import TestCase
from django.urls import reverse
from django.test.client import Client

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from signup.models import User


class TestSignupCreateView(TestCase):
    def setUp(self):
        client = Client()

#ログイン状態でアクセス
    def test_name_login_user(self):
        self.user = User.objects.create_user("sample", "sample@gmail.com", "pass")
        self.client.login(username="sample", password="pass")
        response = self.client.get(reverse('signup:new'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('eat:index'))

    def test_url(self):
        response = self.client.post('/signup/new/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup/signup_new.html')

    def test_name(self):
        response = self.client.post(reverse('signup:new'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup/signup_new.html')

    def test_url_confirm(self):
        data = {
            "username": "sample",
            "email": "sample@gmail.com",
            "password1": "test_password",
            "password2":"test_password",
            "next":"confirm",
            }
        response = self.client.post('/signup/new/', data=data)
        self.assertEqual(response.status_code, 200)


    def test_name_confirm(self):
        data = {
            "username": "sample",
            "email": "sample@gmail.com",
            "password1": "test_password",
            "password2":"test_password",
            "next":"confirm",
            }
        response = self.client.post(reverse('signup:new'), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "signup/signup_regist.html")
        self.assertContains(response, "sample")
        self.assertContains(response, "sample@gmail.com")

    def test_name_confirm_none_data(self):
        data = {
            "next": "confirm",
        }
        response = self.client.post(reverse('signup:new'), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "signup/signup_new.html")

    def test_url_regist(self):
        data = {
            "username": "sample",
            "email": "sample@gmail.com",
            "password1": "test_password",
            "password2":"test_password",
            "next":"regist",
            }
        response = self.client.post('/signup/new/', data=data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('signup:login'))

    def test_name_regist(self):
        data = {
            "username": "sample",
            "email": "sample@gmail.com",
            "password1": "test_password",
            "password2":"test_password",
            "next":"regist",
            }
        response = self.client.post(reverse('signup:new'), data=data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('signup:login'))
        messages = list(response.context["messages"])
        self.assertEqual(str(messages[0]), "会員登録が完了しました。ユーザー名とパスワードを入力してログインしてください")
        self.client.login(username="sample", password="test_password")
        response = self.client.get(reverse('eat:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "eat/recipe_list.html")

    def test_name_regist_none_data(self):
        data = {
            "next":"regist",
            }
        response = self.client.post(reverse('signup:new'), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "signup/signup_new.html")

    def test_name_regist_not_login(self):
        data = {
            "username": "sample",
            "email": "sample@gmail.com",
            "password1": "test_password",
            "password2":"test_password",
            "next":"regist",
            }
        response = self.client.post(reverse('signup:new'), data=data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('signup:login'))
        messages = list(response.context["messages"])
        self.assertEqual(str(messages[0]), "会員登録が完了しました。ユーザー名とパスワードを入力してログインしてください")
        self.client.login(username="samplee", password="test_passwordd")
        response = self.client.get(reverse('eat:index'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/signup/login/?next=/eat/")

    def test_url_back(self):
        data = {
            "username": "sample",
            "email": "sample@gmail.com",
            "password1": "test_password",
            "password2":"test_password",
            "next":"back",
            }
        response = self.client.post('/signup/new/', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "signup/signup_new.html")
        self.assertContains(response, "sample")
        self.assertContains(response, "sample@gmail.com")

    def test_name_back(self):
        data = {
            "username": "sample",
            "email": "sample@gmail.com",
            "password1": "test_password",
            "password2":"test_password",
            "next":"back",
            }
        response = self.client.post(reverse('signup:new'), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "signup/signup_new.html")
        self.assertContains(response, "sample")
        self.assertContains(response, "sample@gmail.com")

    def test_url_none_next(self):
        data = {
            "username": "sample",
            "email": "sample@gmail.com",
            "password1": "test_password",
            "password2":"test_password",
            }
        response = self.client.post('/signup/new/', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/signup/login/")

    def test_name_none_next(self):
        data = {
            "username": "sample",
            "email": "sample@gmail.com",
            "password1": "test_password",
            "password2":"test_password",
            }
        response = self.client.post(reverse('signup:new'), data=data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/signup/login/")



class TestSignupLoginView(TestCase):
    def setUp(self):
        client = Client()
        self.user = User.objects.create_user("sample", "sample@gmail.com", "pass")

    def test_url(self):
        data = {
            "username" : "sample",
            "password" : "pass",
            }
        response = self.client.post('/signup/login/', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/signup/top/")

    def test_name(self):
        data = {
            "username" : "sample",
            "password" : "pass",
            }
        response = self.client.post(reverse('signup:login'), data=data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/signup/top/")

    def test_name_success_messages(self):
        data = {
            "username" : "sample",
            "password" : "pass",
            }
        response = self.client.post(reverse('signup:login'), data=data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, "/signup/top/")
        messages = list(response.context["messages"])
        self.assertEqual(str(messages[0]), "ログインしました")

    def test_name_not_equal_pass(self):
        data = {
            "username" : "sample",
            "password" : "passs",
            }
        response = self.client.post(reverse('signup:login'), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "login.html")
        #contextの書き方
        self.assertContains(response, "username")

    def test_name_error_messages(self):
        data = {
            "username" : "sample",
            "password" : "passs",
            }
        response = self.client.post(reverse('signup:login'), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "login.html")
        messages = list(response.context["messages"])
        self.assertEqual(str(messages[0]), "ログインできませんでした。正しいパスワードとユーザー名を入力してください")


    def test_name_get(self):
        data = {
            "username" : "sample",
            "password" : "pass",
            }
        response = self.client.get(reverse('signup:login'), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "login.html")

    def test_name_none_required(self):
        data = {
            "username" : "sample",
            }
        response = self.client.post(reverse('signup:login'), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "login.html")
        self.assertFormError(response, 'form', 'password', 'このフィールドは必須です。')
        self.assertContains(response, "username")


    def test_name_login(self):
        self.client.login(username="sample", password="pass")
        response = self.client.get(reverse('signup:login'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/eat/")

class TestSignupLogoutView(TestCase):
    def setUp(self):
        client = Client()
        self.user = User.objects.create_user("sample", "sample@gmail.com", "pass")

    def test_url(self):
        self.client.login(username="sample", password="pass")
        response = self.client.get("/signup/logout/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "signup/top.html")

    def test_name(self):
        self.client.login(username="sample", password="pass")
        response = self.client.get(reverse('signup:logout'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "signup/top.html")


class TestSignupDetailView(TestCase):
    def setUp(self):
        client = Client()
        self.user = User.objects.create_user("sample", "sample@gmail.com", "pass")

    def test_url(self):
        self.client.login(username="sample", password="pass")
        response = self.client.get("/signup/detail/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "signup/signup_detail.html")

    def test_name(self):
        self.client.login(username="sample", password="pass")
        response = self.client.get(reverse("signup:detail"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "signup/signup_detail.html")

    def test_mame_not_login(self):
        response = self.client.get(reverse('signup:detail'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/signup/login/?next=/signup/detail/")

class TestSignupUpdateView(TestCase):
    def setUp(self):
        client = Client()
        self.user = User.objects.create_user("sample", "sample@gmail.com", "pass")
        self.user2 = User.objects.create_user("sample2", "sample@gmail.com2", "pass2")

    def test_url_none_object(self):
        self.client.login(username="sample", password="pass")
        response = self.client.get("/signup/update/2")
        self.assertEqual(response.status_code, 403)
        self.client.login(username="sample2", password="pass2")
        response = self.client.get("/signup/update/2")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup/signup_update.html')

    def test_name_none_object(self):
        self.client.login(username="sample", password="pass")
        response = self.client.get(reverse('signup:update', kwargs={'pk': 2}),)
        self.assertEqual(response.status_code, 403)

    def test_url(self):
        self.client.login(username="sample", password="pass")
        response = self.client.get("/signup/update/1")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "signup/signup_update.html")

    def test_name(self):
        self.client.login(username="sample", password="pass")
        response = self.client.get(reverse('signup:update', kwargs={'pk': 1}),)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "signup/signup_update.html")
        self.assertEqual(str(response.context["user"]), "sample")
        self.assertEqual(response.context['form'].initial['username'], 'sample')
        self.assertEqual(response.context['form'].initial['email'], 'sample@gmail.com')

    def test_name_update_username(self):
        self.client.login(username="sample", password="pass")
        with open(os.path.join(os.environ['HOME'], 'Desktop/Picture/illustration-2541681_1280.jpg'), 'rb') as img:
            data = {
                "username": "update_user",
                "icon": "",
                "email": "sample@gmail.com",
                }
            response = self.client.post(
                reverse('signup:update', kwargs={'pk': 1}), data, follow=True
                )
            self.assertEqual(response.status_code, 200)
            self.assertRedirects(response, reverse("eat:index"))
            messages = list(response.context["messages"])
            self.assertEqual(str(messages[0]), "ユーザー情報を変更しました")
            self.assertEqual(User.objects.get(id=1).username, 'update_user')

    def test_name_update_icon(self):
        self.client.login(username="sample", password="pass")
        with open(os.path.join(os.environ['HOME'], 'Desktop/Picture/illustration-2541681_1280.jpg'), 'rb') as img:
            data = {
                "username": "sample",
                "icon": img,
                "email": "sample@gmail.com",
                }
            response = self.client.post(
                reverse('signup:update', kwargs={'pk': 1}), data, follow=True
                )
            self.assertEqual(response.status_code, 200)
            self.assertRedirects(response, reverse("eat:index"))

    def test_login_other(self):
        self.client.login(username="sample2", password="pass")
        response = self.client.get(reverse('signup:update', kwargs={'pk':1}))
        self.assertEqual(response.status_code, 403)

    def test_name_not_login(self):
        response = self.client.get(reverse('signup:update', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 403)


class TestSignupPasswordChangeView(TestCase):
    def setUp(self):
        client = Client()
        self.user = User.objects.create_user("sample", "sample@gmail.com", "pass")

    def test_url(self):
        self.client.login(username="sample", password="pass")
        response = self.client.get("/signup/change/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "signup/signup_PasswordChange.html")

    def test_name(self):
        self.client.login(username="sample", password="pass")
        response = self.client.get(reverse('signup:changepass'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "signup/signup_PasswordChange.html")

    def test_name_success_messages(self):
        self.client.login(username="sample", password="pass")
        data = {
            "old_password": "pass",
            "new_password1": "new_password",
            "new_password2": "new_password",
            }
        response = self.client.post(reverse("signup:changepass"), data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse("eat:index"))
        messages = list(response.context["messages"])
        self.assertEqual(str(messages[0]), "パスワードを変更しました")
        self.client.logout()
        self.client.login(username="sample", password="new_password")
        response = self.client.get(reverse('eat:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'eat/recipe_list.html')

    def test_name_not_login(self):
        response = self.client.get(reverse('signup:changepass'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/signup/login/?next=/signup/change/")

class TestSignupDeleteView(TestCase):
    def setUp(self):
        client = Client()
        self.user = User.objects.create_user("sample", "sample@gmail.com", "pass")
        self.user2 = User.objects.create_user("sample2", "sample@gmail.com2", "pass2")

    def test_url_none_object(self):
        self.client.login(username="sample", password="pass")
        response = self.client.get("/signup/delete/2")
        self.assertEqual(response.status_code, 403)
        #ユーザー２でアクセス
        self.client.login(username="sample2", password="pass2")
        response = self.client.get("/signup/delete/2")
        self.assertEqual(response.status_code, 200)

    def test_name_none_object(self):
        self.client.login(username="sample", password="pass")
        response = self.client.get(reverse('signup:delete', kwargs={'pk': 2}),)
        self.assertEqual(response.status_code, 403)


    def test_url_get(self):
        self.client.login(username="sample", password="pass")
        response = self.client.get("/signup/delete/1")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "signup/signup_delete.html")

    def test_name_get(self):
        self.client.login(username="sample", password="pass")
        response = self.client.get(reverse("signup:delete", kwargs={'pk':1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "signup/signup_delete.html")

    def test_name_post_delete(self):
        self.client.login(username="sample", password="pass")
        response = self.client.post(reverse("signup:delete", kwargs={'pk':1}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("signup:new"))
        self.client.login(username="sample", password="pass")
        response = self.client.get(reverse("eat:index"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/signup/login/?next=/eat/")

    def test_name_success_messages(self):
        self.client.login(username="sample", password="pass")
        response = self.client.post(reverse("signup:delete", kwargs={'pk':1}), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse("signup:new"))
        messages = list(response.context["messages"])
        self.assertEqual(str(messages[0]), "退会しました。再度アプリを利用するには会員登録が必要です")


    def test_name_not_login(self):
        response = self.client.get(reverse("signup:delete", kwargs={'pk':1}))
        self.assertEqual(response.status_code, 403)

class TestPasswordResetView(TestCase):
    def setUp(self):
        client = Client()
        self.user = User.objects.create_user("sample", "sample@gmail.com", "pass")

    def test_url(self):
        data = {
            "email": "sample@gmail.com",
        }
        response = self.client.post("/signup/password_reset/", data=data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('signup:password_reset_done'))

    def test_name(self):
        data = {
            "email": "sample@gmail.com",
            }
        response = self.client.post(reverse("signup:password_reset"), data=data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('signup:password_reset_done'))

    def test_url_none_data(self):
        response = self.client.post("/signup/password_reset/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/password_reset_form.html')

    def test_name_none_data(self):
        response = self.client.post(reverse("signup:password_reset"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/password_reset_form.html')




class TestPasswordResetConfirmView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("sample", "sample@gmail.com", "pass")


    def test_name(self):
        token_generator = PasswordResetTokenGenerator()
        token = token_generator.make_token(self.user)
        uidb64 = urlsafe_base64_encode(force_bytes(self.user.pk))
        data = {
            'new_password1': "test_password",
            'new_password2': "test_password",
            }
        response = self.client.post(
            reverse('signup:password_reset_confirm', kwargs={'uidb64': uidb64, 'token': 'set-password'}), data=data
            )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('signup:password_reset_complate'))



class TestTemplateView(TestCase):
    def test_url(self):
        response = self.client.get("/signup/top/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "signup/top.html")

    def test_name(self):
        response = self.client.get("/signup/top/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "signup/top.html")
