from django.urls import path
from . import views

urlpatterns = [
    path("", views.adminpanel, name="adminpanel"),
    path("login", views.admin_login, name="login"),
    path("test", views.test, name="test"),
    path("logout", views.logout_admin, name="logout"),
    path("addemployee", views.AddEmployee, name="addemployee"),
    path("CalculateSalary", views.CalculateSalary, name="CalculateSalary"),
    path("salaryview", views.salaryview, name="salaryview"),
    path("Employeelist", views.Employeelist, name="Employeelist"),
    path("EditEmployee/<int:emp_id>", views.EditEmployee, name="EditEmployee"),
    path("deleteEmployee/<int:emp_id>", views.deleteEmployee, name="deleteEmployee"),
]
