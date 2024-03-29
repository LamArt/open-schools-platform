# Generated by Django 3.2.3 on 2022-06-28 12:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from safedelete import HARD_DELETE
from safedelete.config import DELETED_VISIBLE


def create_profiles_for_employees(apps, schema_editor):
    EmployeeProfile = apps.get_model("employees", "employeeprofile")
    User = apps.get_model("users", "User")
    db_alias = schema_editor.connection.alias
    qs = User.objects.using(db_alias).all(force_visibility=DELETED_VISIBLE)
    for i in qs:
        employee_profile = EmployeeProfile()
        employee_profile.user = i
        employee_profile.name = i.name
        employee_profile.save(using=db_alias)


def delete_employees_profiles(apps, schema_editor):
    EmployeeProfile = apps.get_model("employees", "employeeprofile")
    db_alias = schema_editor.connection.alias
    EmployeeProfile.objects.using(db_alias).all().delete(force_policy=HARD_DELETE)


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('employees', '0004_employees'),
    ]

    operations = [
        migrations.RunPython(create_profiles_for_employees, delete_employees_profiles),

        migrations.AlterField(
            model_name='employee',
            name='employee_profile',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='employees',
                                    to="employees.employeeprofile", default=None),
        ),
    ]
