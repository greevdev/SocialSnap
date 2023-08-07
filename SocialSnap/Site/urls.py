from django.conf.urls.static import static
from django.urls import path, include
from django.conf import settings
from .views import landing_page, dashboard_page, UserProfileView, my_profile, FollowUserView, UnfollowUserView, \
    search_view, settings_view, EditProfileView, delete_account, change_password


urlpatterns = [
    path('', landing_page, name='landing page'),
    path('dashboard/', dashboard_page, name='dashboard page'),
    path('profile/<str:username>/', include([
        path('', UserProfileView.as_view(), name='user profile'),
        path('follow/', FollowUserView.as_view(), name='follow user'),
        path('unfollow/', UnfollowUserView.as_view(), name='unfollow user'),
        path('edit/', EditProfileView.as_view(), name='edit profile'),
        path('delete/', delete_account, name='delete profile'),
        path('password/', change_password, name='change password'),
    ])),
    path('myprofile/', my_profile, name='my profile'),
    path('search/', search_view, name='search'),
    path('settings/', settings_view, name='settings'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
