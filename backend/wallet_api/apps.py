from django.apps import AppConfig


class WalletApiConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "wallet_api"
    def ready(self):
        from . import signals
