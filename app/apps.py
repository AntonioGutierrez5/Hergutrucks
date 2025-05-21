from django.apps import AppConfig

class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'  # Asegúrate que este sea el nombre de tu app real

    def ready(self):
        import app.signals  # Importa tu archivo de señales aquí
