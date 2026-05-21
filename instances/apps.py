from django.apps import AppConfig


class InstancesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'instances'

    def ready(self):
        import instances.signals  # noqa: F401
