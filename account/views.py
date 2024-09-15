from django.shortcuts import redirect
from django.views.generic.edit import CreateView
from django.contrib.auth import logout
from django.urls import reverse_lazy

from .forms import RegisterForm
from .models import Profile


class Register(CreateView):
    model = Profile
    form_class = RegisterForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("account:login")


def log_out(request):
    logout(request)
    return redirect("blog:home")
