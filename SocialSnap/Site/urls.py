from django.urls import path, include
from .views import landing_page, dashboard_page, UserProfileView, my_profile, FollowUserView, UnfollowUserView

urlpatterns = [
    path('', landing_page, name='landing page'),
    path('dashboard/', dashboard_page, name='dashboard page'),
    path('profile/<str:username>/', include([
        path('', UserProfileView.as_view(), name='user profile'),
        path('follow/', FollowUserView.as_view(), name='follow user'),
        path('unfollow/', UnfollowUserView.as_view(), name='unfollow user'),
    ])),
    path('myprofile/', my_profile, name='my profile'),
]
