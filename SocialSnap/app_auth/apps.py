from django.apps import AppConfig


class AppAuthConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'SocialSnap.app_auth'

    def ready(self):
        import SocialSnap.app_auth.signals
