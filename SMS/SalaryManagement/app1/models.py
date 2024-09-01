from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.db.models.signals import post_save
from django.dispatch import receiver


class admin_data(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    profile = models.CharField(max_length=50)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.name


class Employee(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    mobile = models.CharField(max_length=13)
    address = models.CharField(max_length=200)
    base_salary = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.name


class Salary(models.Model):
    MONTH = (
        ("january", "january"),
        ("february", "february"),
        ("march", "march"),
        ("april", "april"),
        ("may", "may"),
        ("june", "june"),
        ("july", "july"),
        ("august", "august"),
        ("september", "september"),
        ("october", "october"),
        ("november", "november"),
        ("december", "december"),
    )
    YEAR = (
        ("2023", "2023"),
        ("2024", "2024"),
        ("2025", "2025"),
        ("2026", "2026"),
        ("2027", "2027"),
        ("2028", "2028"),
        ("2029", "2029"),
        ("2030", "2030"),
    )
    employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE)
    month = models.CharField(max_length=50, choices=MONTH)
    year = models.CharField(max_length=50, choices=YEAR)
    total_working_days = models.PositiveIntegerField(default=0)
    total_leave_taken = models.PositiveIntegerField(default=0)
    overtime = models.PositiveIntegerField(default=0)
    Total_salary_made = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)
    is_salary_calculated = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return self.employee_id.name


# @receiver(post_save, sender=Salary)
# def calculatesalary(sender, instance, created, **kwargs):
#     if created:
#         instance.Total_salary_made = 10 * (
#             instance.total_working_days
#             - instance.total_leave_taken
#             + instance.overtime / 8
#         )
#         instance.is_salary_calculated = 1
#         instance.save()
