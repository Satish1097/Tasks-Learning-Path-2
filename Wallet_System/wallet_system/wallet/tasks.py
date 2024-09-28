import time
from celery import shared_task
from django.core.management import call_command


# @shared_task
# def test_task():
#     print("Task executed by solar schedule.")


@shared_task()
def check_pay_status():
    starttime = time.time()
    print("Starting pay status check...")

    try:
        call_command("paystatus")
        print("Pay status updated successfully.")
    except Exception as e:
        print(f"Error while updating pay status: {e}")

    endtime = time.time()
    execution_time = endtime - starttime
    print(f"Execution time: {execution_time:.2f} seconds")

    return "done"
