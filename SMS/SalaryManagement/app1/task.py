from celery import shared_task
from django.core.management import call_command


@shared_task
def calculate_salaries_task():
    call_command("calculate_salaries")
