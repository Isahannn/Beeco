from django.apps import AppConfig

class BeecoAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'beeco_app'

    def ready(self):
        import beeco_app.signals