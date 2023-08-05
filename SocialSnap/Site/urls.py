from django.urls import path, include
from .views import landing_page, dashboard_page, UserProfileView, my_profile

urlpatterns = [
    path('', landing_page, name='landing page'),
    path('dashboard/', dashboard_page, name='dashboard page'),
    path('profile/<str:username>/', UserProfileView.as_view(), name='user profile'),
    path('myprofile/', my_profile, name='my profile'),

]
