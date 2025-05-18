from django.apps import AppConfig

class ApiConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "App"

    def ready(self):
        import App.signals  # Ensure signals are loaded
