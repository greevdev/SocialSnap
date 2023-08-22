from django.contrib import admin
from .models import Post, Comment


class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'content', 'image', 'creator_id', 'created_at']
    list_filter = ['creator_id', 'created_at']


class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'content', 'creator_id', 'created_at']
    list_filter = ['creator_id', 'created_at']


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
