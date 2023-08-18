from django.conf.urls.static import static
from django.urls import path, include
from django.conf import settings
from .views import landing_page, home_page, about_page, UserProfileView, my_profile, FollowUserView, UnfollowUserView, \
    search_view, settings_view, EditProfileView, delete_account, change_password, create_post, LikePostView, \
    EditPostView, DeletePostView, UserConnectionsView, ViewPostView, add_comment, EditCommentView, DeleteCommentView

urlpatterns = [
    path('', landing_page, name='landing page'),
    path('about/', about_page, name='about page'),
    path('home/', home_page, name='home page'),
    path('profile/<str:username>/', include([
        path('', UserProfileView.as_view(), name='user profile'),
        path('follow/', FollowUserView.as_view(), name='follow user'),
        path('unfollow/', UnfollowUserView.as_view(), name='unfollow user'),
        path('edit/', EditProfileView.as_view(), name='edit profile'),
        path('delete/', delete_account, name='delete profile'),
        path('password/', change_password, name='change password'),
        path('createpost/', create_post, name='create post'),
        path('connections/', UserConnectionsView.as_view(), name='connections'),
    ])),
    path('myprofile/', my_profile, name='my profile'),
    path('search/', search_view, name='search'),
    path('settings/', settings_view, name='settings'),
    path('like/<int:post_id>/', LikePostView.as_view(), name='like post'),
    path('editpost/<int:post_id>/', EditPostView.as_view(), name='edit post'),
    path('deletepost/<int:post_id>/', DeletePostView.as_view(), name='delete post'),
    path('viewpost/<int:post_id>/', ViewPostView.as_view(), name='view post'),
    path('comment/<int:post_id>/', add_comment, name='add comment'),
    path('editcomment/<int:comment_id>/', EditCommentView.as_view(), name='edit comment'),
    path('deletecomment/<int:comment_id>/', DeleteCommentView.as_view(), name='delete comment'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
