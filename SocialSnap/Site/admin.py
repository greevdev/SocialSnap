from django.contrib import admin
from .models import Post


class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'content', 'image', 'creator_id', 'created_at']
    list_filter = ['creator_id', 'created_at']


admin.site.register(Post, PostAdmin)
