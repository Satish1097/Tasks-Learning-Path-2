from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from app1.models import admin_data, Salary, Employee
from .forms import AddEmpForm, SalaryForm
from django.db.models.functions import Lower


def admin_login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        print(email, password)
        try:
            admin_user = admin_data.objects.get(email=email)
            if admin_user.check_password(password):
                request.session["user"] = admin_user.id
                return redirect("adminpanel")
            else:
                messages.error(request, "Invalid Credential")
                return render(request, "login.html")
        except admin_data.DoesNotExist:
            messages.error(request, "Invalid credentials")
            return render(request, "login.html")
    return render(request, "login.html")


def logout_admin(request):
    del request.session["user"]
    return redirect("login")


def AddEmployee(request):
    user = request.session.get("user")
    if user is not None:
        if request.method == "POST":
            form = AddEmpForm(request.POST)
            if form.is_valid():
                form.save()
            else:
                messages.error("Invalid data entered in form")
                return redirect("login")
        else:
            form = AddEmpForm()
        return render(request, "AddEmp.html", {"form": form})
    else:
        messages.error(request, "Login to Perform Action")
        return redirect("login")


def CalculateSalary(request):
    user = request.session.get("user")
    if user is not None:
        if request.method == "POST":
            form = SalaryForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Calculated")
                return redirect("CalculateSalary")
            else:
                messages.error(request, "Invalid Form Data")
                return redirect("CalculateSalary")
        else:
            form = SalaryForm()
            return render(request, "AddSalary.html", {"form": form})
    else:
        return redirect("login")


def salaryview(request):
    user = request.session.get("user")
    if user is not None:
        salaries = Salary.objects.all()
        return render(request, "salarydetail.html", {"salaries": salaries})
    else:
        return redirect("login")


def Employeelist(request):
    user = request.session.get("user")
    if user is not None:
        employees = Employee.objects.all().order_by(Lower("name"))
        return render(request, "Employee.html", {"employees": employees})
    else:
        return redirect("login")


def EditEmployee(request, emp_id):
    user = request.session.get("user")
    if user is not None:
        employee = Employee.objects.get(id=emp_id)
        if request.method == "POST":
            form = AddEmpForm(request.POST, instance=employee)
            if form.is_valid():
                form.save()
                return redirect("Employeelist")
        else:
            form = AddEmpForm(instance=employee)
            return render(request, "AddEmp.html", {"form": form})
    else:
        return redirect("login")


def deleteEmployee(request, emp_id):
    user = request.session.get("user")
    if user is not None:
        employee = Employee.objects.get(id=emp_id)
        employee.delete()
        return redirect("Emloyeelist")
    else:
        return redirect("login")


def adminpanel(request):
    user = request.session.get("user")
    if user is not None:
        return render(request, "Dashboard.html")
    else:
        return redirect("login")
