from django.urls import path
from .views import register_view, login_view

urlpatterns = [
    path('register/', register_view, name='register page'),
    path('login/', login_view, name='login page'),
    # path('logout/', LogoutUserView.as_view(), name='logout_user'),
]
