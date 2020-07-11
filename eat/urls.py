from django.contrib import admin
from django.urls import path
from eat.views import EatListView, EatDetailView, EatCreateView, EatUpdateView, EatDeleteView

app_name = "eat"

urlpatterns = [
    path('', EatListView.as_view(), name="index"),
    path('detail/<int:pk>/', EatDetailView.as_view(), name="detail"),
    path('create/', EatCreateView.as_view(), name="create"),
    path('update/<int:pk>/', EatUpdateView.as_view(), name="update"),
    path('delete/<int:pk>/', EatDeleteView.as_view(), name="delete"),

]
