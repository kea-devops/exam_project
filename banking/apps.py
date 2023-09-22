from django.apps import AppConfig
from django.db.models.signals import post_migrate

class BankingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'banking'

    def ready(self):
        # populate database with initial entities
        from banking.signals import populate_models
        post_migrate.connect(populate_models, sender=self)