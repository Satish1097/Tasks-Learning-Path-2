from django.urls import path
from . import views

urlpatterns = [
    path("", views.admin_login, name="login"),
    path("logout", views.logout_admin, name="logout"),
    path("adminpanel", views.adminpanel, name="adminpanel"),
    path("addemployee", views.AddEmployee, name="addemployee"),
    path("CalculateSalary", views.CalculateSalary, name="CalculateSalary"),
    path("salaryview", views.salaryview, name="salaryview"),
    path("Employeelist", views.Employeelist, name="Employeelist"),
    path("EditEmployee/<int:emp_id>", views.EditEmployee, name="EditEmployee"),
]
