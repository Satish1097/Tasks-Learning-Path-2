from django import forms
from .models import admin_data, Employee, Salary


class AdminsCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = admin_data
        fields = ["name", "email", "password"]

    def save(self, commit=True):
        admin = super().save(commit=False)
        admin.set_password(self.cleaned_data["password"])  # Hash the password
        if commit:
            admin.save()
        return admin


class AddEmpForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ["name", "email", "mobile", "address", "base_salary"]

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if not name:
            raise forms.ValidationError("name required")
        return name

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not email:
            raise forms.ValidationError("email required")
        return email

    def clean_mobile(self):
        mobile = self.cleaned_data.get("mobile")
        if not mobile:
            raise forms.ValidationError("mobile number required")
        if len(mobile) < 10:
            raise forms.ValidationError("invalid number")
        return mobile

    def clean_address(self):
        address = self.cleaned_data.get("address")
        if not address:
            raise forms.ValidationError("address required")
        return address

    def clean_base_salary(self):
        base_salary = self.cleaned_data.get("base_salary")
        if not base_salary:
            raise forms.ValidationError("base_salary required")
        elif base_salary < 0:
            raise forms.ValidationError("Base_salary should be greater than 0")
        else:
            return base_salary


class SalaryForm(forms.ModelForm):
    class Meta:
        model = Salary
        fields = [
            "employee_id",
            "month",
            "year",
            "total_working_days",
            "total_leave_taken",
            "overtime",
        ]

    def clean_month(self):
        month = self.cleaned_data.get("month")
        if not month:
            raise forms.ValidationError("month is required")
        return month

    def clean_year(self):
        year = self.cleaned_data.get("year")
        if not year:
            raise forms.ValidationError("year is required")
        return year

    def clean_working_day(self):
        working_day = self.cleaned_data.get("total_working_days")
        if not working_day:
            raise forms.ValidationError("working_day is required")
        return working_day

    def clean_leave_taken(self):
        leave = self.cleaned_data.get("total_leave_taken")
        if not leave:
            raise forms.ValidationError("total_leave_taken is required")
        return leave

    def clean_overtime(self):
        overtime = self.cleaned_data.get("overtime")
        if not overtime:
            raise forms.ValidationError("overtime is required")
        return overtime
