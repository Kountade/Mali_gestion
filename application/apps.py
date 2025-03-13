
from django.apps import AppConfig

class TonApplicationConfig(AppConfig):
    name = 'application'

    def ready(self):
        import application.signals  # Remplace 'ton_application' par le nom de ton application
