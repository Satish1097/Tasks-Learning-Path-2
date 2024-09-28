from __future__ import absolute_import, unicode_literals
import os
from celery import Celery


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wallet_system.settings")

app = Celery("wallet_system")
app.conf.enable_utc = False

app.conf.update(timezone="Asia/Kolkata")

app.config_from_object("django.conf:settings", namespace="CELERY")


# app.conf.beat_schedule = {
#     "add-every-30-seconds": {
#         "task": "wallet.tasks.check_pay_status",
#         "schedule": 10.0,
#         # "args": (16, 16),
#     },
# }
app.conf.timezone = "Asia/Kolkata"

app.autodiscover_tasks("")


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
