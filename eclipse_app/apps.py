from django.apps import AppConfig


class EclipseAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'eclipse_app'

    def ready(self):
        import eclipse_app.signals