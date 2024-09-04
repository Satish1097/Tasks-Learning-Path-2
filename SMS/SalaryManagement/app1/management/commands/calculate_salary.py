from django.core.management.base import BaseCommand
from app1.models import Salary


class Command(BaseCommand):
    help = "Calculate salaries based on specific criteria"

    def handle(self, *args, **options):
        uncalculated_salaries = Salary.objects.filter(is_salary_calculated=0)

        for salary in uncalculated_salaries:
            total_salary_made = 10 * (
                salary.total_working_days
                - salary.total_leave_taken
                + salary.overtime / 8
            )
            salary.Total_salary_made = total_salary_made
            salary.is_salary_calculated = 1
            salary.save()

            self.stdout.write(
                self.style.SUCCESS(f"Salary calculated for ID {salary.id}")
            )
        self.stdout.write(self.style.SUCCESS("Salary calculation completed"))
