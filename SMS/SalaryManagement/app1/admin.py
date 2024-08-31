from django.contrib import admin
from app1.models import admin_data, Salary, Employee
from .forms import AdminsCreationForm

# Register your models here.
admin.site.register(Salary)
admin.site.register(Employee)


class AdminsAdmin(admin.ModelAdmin):
    form = AdminsCreationForm
    list_display = ["name", "email", "password"]


admin.site.register(admin_data, AdminsAdmin)
