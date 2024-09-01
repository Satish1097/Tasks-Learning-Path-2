# Generated by Django 5.0.7 on 2024-08-31 09:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0003_rename_admins_admin_data'),
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('mobile', models.IntegerField()),
                ('address', models.CharField(max_length=200)),
                ('base_salary', models.DecimalField(decimal_places=2, max_digits=8)),
            ],
        ),
        migrations.CreateModel(
            name='Salary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('month', models.CharField(choices=[('january', 'january'), ('february', 'february'), ('march', 'march'), ('april', 'april'), ('may', 'may'), ('june', 'june'), ('july', 'july'), ('august', 'august'), ('september', 'september'), ('october', 'october'), ('november', 'november'), ('december', 'december')], max_length=50)),
                ('year', models.CharField(choices=[('2023', '2023'), ('2024', '2024'), ('2025', '2025'), ('2026', '2026'), ('2027', '2027'), ('2028', '2028'), ('2029', '2029'), ('2030', '2030')], max_length=50)),
                ('total_working_days', models.IntegerField(default=0)),
                ('total_leave_taken', models.IntegerField(default=0)),
                ('overtime', models.IntegerField(default=0)),
                ('Total_salary_made', models.DecimalField(decimal_places=2, max_digits=8)),
                ('employee_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.employee')),
            ],
        ),
    ]