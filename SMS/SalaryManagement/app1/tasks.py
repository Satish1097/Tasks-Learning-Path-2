from celery import shared_task, group
from app1.models import Salary, Employee
import time
from django.core.mail import send_mail
from SalaryManagement import settings
from decimal import Decimal

# from django.core.management import call_command


@shared_task
def process_salary(salary_id):
    starttime = time.time()
    print(starttime)
    salary = Salary.objects.get(id=salary_id)
    total_salary_made = (
        salary.employee_id.base_salary
        / salary.total_working_days
        * Decimal.from_float(
            salary.total_working_days - salary.total_leave_taken + salary.overtime / 8
        )
    )
    salary.Total_salary_made = total_salary_made
    salary.is_salary_calculated = 1
    salary.save()
    endtime = time.time()
    print(endtime)


@shared_task
def run_parallel_salary_processing():
    start_time = time.time()
    salaries_to_process = list(
        Salary.objects.filter(is_salary_calculated=0).values_list("id", flat=True)
    )
    tasks = [process_salary.s(salary_id) for salary_id in salaries_to_process]

    group_tasks = group(tasks)
    group_result = group_tasks.apply_async()

    end_time = time.time()
    execution_time = end_time - start_time
    print(f"The group of tasks took {execution_time} seconds to execute.")
    return group_result.id


@shared_task
def send_mail_fun():
    employees = Employee.objects.all()
    for employee in employees:
        mail_subject = "Salary Report"
        message = "salary details"
        to_email = employee.email
        send_mail(
            subject=mail_subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[to_email],
            fail_silently=True,
        )
        return "email sent"


# @shared_task
# def calculate_salaries_task():
#     starttime = time.time()
#     print("inside celery")
#     call_command("calculate_salary")
#     endtime = time.time()
#     execution_time = endtime - starttime
#     print(f"The calculate_salaries_task took {execution_time} seconds to execute.")
#     return "done"
