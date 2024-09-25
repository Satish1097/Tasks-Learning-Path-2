from django.contrib.auth.models import User
from .models import *
from celery import shared_task
import time
from django.core.management import call_command


import logging

logger = logging.getLogger(__name__)


def cron_task():
    print("hello")
    logger.info("")


@shared_task
def calculate_salaries_task():
    starttime = time.time()
    print("inside celery")
    call_command("paystatus")
    endtime = time.time()
    execution_time = endtime - starttime
    print(f"The calculate_salaries_task took {execution_time} seconds to execute.")
    return "done"
