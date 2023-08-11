from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.private_dashboard, name='private dashboard'),
]
