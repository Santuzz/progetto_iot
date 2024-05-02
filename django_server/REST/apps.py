from django.apps import AppConfig


class RestConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "REST"

    def ready(self):
        import REST.signals
