from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from SocialSnap.app_auth.models import User


def landing_page(request):
    return render(request, template_name='common/landing.html')


@login_required
def dashboard_page(request):
    context = {
        'username': request.user.get_username()
    }

    return render(request, context=context, template_name='common/dashboard.html')


class UserProfileView(View):
    template_name = 'common/profile.html'

    def get(self, request, username):
        user = get_object_or_404(User, username=username)

        context = {
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
        }

        return render(request, self.template_name, context=context)


@login_required
def my_profile(request):
    username = request.user.username

    url = reverse('user profile', kwargs={'username': username})

    return redirect(url)
