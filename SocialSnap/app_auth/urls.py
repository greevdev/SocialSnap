from django.urls import path
from .views import RegisterView, LoginView, LogoutView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register page'),
    path('login/', LoginView.as_view(), name='login page'),
    path('logout/', LogoutView.as_view(), name='logout user'),
]
