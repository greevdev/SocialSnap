from django.contrib.auth.models import Group, Permission
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from SocialSnap.admin_app.forms import CustomUserCreationForm
from SocialSnap.app_auth.models import User


class CustomUserAdmin(BaseUserAdmin):
    add_form = CustomUserCreationForm

    list_display = ('id', 'username', 'email', 'first_name', 'last_name', 'date_joined', 'last_login',
                    'is_active', 'is_staff', 'is_superuser')
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")
    search_fields = ("username", "first_name", "last_name", "email")
    ordering = ("username",)


admin.site.register(User, CustomUserAdmin)

staff_group, created = Group.objects.get_or_create(name='staff_group')
superuser_group, created = Group.objects.get_or_create(name='superuser_group')

staff_permissions = Permission.objects.filter(codename__in=['delete_post', 'change_post',
                                                            'change_profile', 'change_user',
                                                            'view_user', 'view_group',
                                                            'view_permission', 'view_post',
                                                            'view_profile', 'add_post'])
superuser_permissions = Permission.objects.all()

staff_group.permissions.set(staff_permissions)
superuser_group.permissions.set(superuser_permissions)
