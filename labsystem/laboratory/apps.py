from django.apps import AppConfig


class LaboratoryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'labsystem.laboratory'

    def ready(self):
        import labsystem.laboratory.signals.handlers
        return super(LaboratoryConfig, self).ready()
