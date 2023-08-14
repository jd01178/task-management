from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView

from accounts.forms import UserAuthenticationForm, RegistrationForm
from accounts.mixins import CustomLoginMixin
from accounts.models import User


class UserCreateView(SuccessMessageMixin, CreateView):
    template_name = "accounts/register.html"
    form_class = RegistrationForm
    model = User
    success_message = "You've registered successfully, Thankyou for choosing us."
    success_url = reverse_lazy('accounts:login')


class UserLoginView(CustomLoginMixin, SuccessMessageMixin, LoginView):
    template_name = 'accounts/login.html'
    authentication_form = UserAuthenticationForm
    next_page = reverse_lazy("task:index")


class LogoutView(View):

    def get(self, *args, **kwargs):
        logout(self.request)
        messages.info(self.request, "You've logged out successfully.")
        return redirect('accounts:login')
