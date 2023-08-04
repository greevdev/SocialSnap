from django.contrib.auth.decorators import login_required
from django.shortcuts import render


def landing_page(request):
    return render(request, template_name='common/landing.html')


def dashboard_page(request):
    context = {
        'username': request.user.get_username()
    }

    return render(request, context=context, template_name='common/dashboard.html')
