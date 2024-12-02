from django.apps import AppConfig


class EmployeeLeaveConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'employee_leave'

def ready(self):
        import employee_leave.signals 