from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

from .forms import RegisterForm


class Register(CreateView):
    form_class = RegisterForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("account:login")


    