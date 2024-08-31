from django.urls import path
from . import views

urlpatterns = [
    path("", views.admin_login, name="login"),
    path("logout", views.logout_admin, name="logout"),
    path("adminpanel", views.adminpannel, name="adminpanel"),
    path("addemployee", views.AddEmployee, name="addemployee"),
    path("CalculateSalary", views.CalculateSalary, name="CalculateSalary"),
    path("salaryview", views.salaryview, name="salaryview"),
]
