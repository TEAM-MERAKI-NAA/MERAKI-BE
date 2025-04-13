from django.apps import AppConfig


class BudgettrackerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'budgettracker'
    verbose_name = 'Budget Tracker'

    def ready(self):
        try:
            import budgettracker.signals
        except ImportError:
            pass
