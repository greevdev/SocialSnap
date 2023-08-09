from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect
from django.views import View
from django.views.generic import FormView

from .forms import RegisterForm
from ..Site.models import Profile


class RegisterView(FormView):
    template_name = 'common/register.html'
    form_class = RegisterForm
    success_url = '/auth/login/'

    def form_valid(self, form):
        user = form.save()
        Profile.objects.create(user=user)

        return super().form_valid(form)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class LoginView(FormView):
    template_name = 'common/login.html'
    form_class = AuthenticationForm
    success_url = '/home/'

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)

        return super().form_valid(form)


class LogoutView(View):
    def get(self, request):
        logout(request)

        return redirect('landing page')
