from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
from .models import User


@receiver(post_save, sender=User)
def assign_groups(sender, instance, **kwargs):
    if instance.is_superuser:
        superuser_group, _ = Group.objects.get_or_create(name='superuser_group')
        instance.groups.add(superuser_group)

    if instance.is_staff:
        staff_group, _ = Group.objects.get_or_create(name='staff_group')
        instance.groups.add(staff_group)
