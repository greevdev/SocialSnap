from django.urls import path, include
from .views import landing_page, dashboard_page

urlpatterns = [
    path('', landing_page, name='landing page'),
    path('dashboard/', dashboard_page, name='dashboard page'),
]
