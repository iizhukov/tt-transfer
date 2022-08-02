from django.apps import AppConfig


class TariffsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api.tariffs'
    verbose_name: str = "Тарифы"
