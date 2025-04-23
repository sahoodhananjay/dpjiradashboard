from django.apps import AppConfig


class QualityboardConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'qualityboard'


    def ready(self):
        print("Starting Scheduler ... ")
        from .jira_scheduler import jira_updater
        jira_updater.start()

