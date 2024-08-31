from django.urls import path
from django.contrib.auth import views

from .views import Register

app_name = "account"
urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("register/", Register.as_view(), name="register"),
]
