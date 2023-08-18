"""SocialSnap URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve
from SocialSnap import settings
from SocialSnap.Site.views import custom_404, custom_500

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('SocialSnap.Site.urls')),
    path('auth/', include('SocialSnap.app_auth.urls')),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_URL}),
]

handler404 = custom_404
handler505 = custom_500

