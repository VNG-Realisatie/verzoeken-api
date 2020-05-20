from django.apps import AppConfig


class UtilsConfig(AppConfig):
    name = "verzoeken.utils"

    def ready(self):
        from . import checks  # noqa
