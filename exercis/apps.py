from django.apps import AppConfig


class ExercisConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "exercis"
    def ready(self) -> None:
        import exercis.signals
        # return super().ready()

