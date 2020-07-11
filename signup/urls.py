
from django.urls import path
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from .views import SignupCreateView, SignupLoginView, SignupDetailView, SignupUpdateView, SignupPasswordChangeView, SignupDeleteView

app_name = "signup"

urlpatterns = [
    path('new/', SignupCreateView.as_view(), name="new"),
    path('login/', SignupLoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(template_name='signup/top.html'), name="logout"),
    path('detail/', SignupDetailView.as_view(), name="detail"),
    path('update/<int:pk>', SignupUpdateView.as_view(), name="update"),
    path('change/', SignupPasswordChangeView.as_view(), name="changepass"),
    path('delete/<int:pk>', SignupDeleteView.as_view(), name="delete"),
    path('password_reset/', PasswordResetView.as_view(success_url=reverse_lazy('signup:password_reset_done')), name="password_reset"),
    path('password_reset/done/', PasswordResetDoneView.as_view(), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(success_url=reverse_lazy('signup:password_reset_complate')), name="password_reset_confirm"),
    path('reset/done/', PasswordResetCompleteView.as_view(), name="password_reset_complate"),
    path('top/', TemplateView.as_view(template_name='signup/top.html'), name="top")
    #path("register/", signupregister, name = "register"),
    #path("register/", SignupDetailView.as_view(), name = "register"),
]
