# Generated by Django 4.2.4 on 2023-08-18 21:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Site', '0004_post_comments'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='likes',
        ),
    ]
