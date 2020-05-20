from django.apps import AppConfig


class SyncConfig(AppConfig):
    name = "verzoeken.sync"

    def ready(self):
        from . import signals  # noqa
