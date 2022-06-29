

# Generated by Django 3.2.3 on 2022-06-28 12:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


def forwards_func(apps, schema_editor):
    # We get the model from the versioned app registry;
    # if we directly import it, it'll be the wrong version
    Employee = apps.get_model("employees", "employee")
    db_alias = schema_editor.connection.alias
    qs = Employee.objects.using(db_alias).all()
    for i in qs:
        i.employee_profile = i.user
        i.save()


def reverse_func(apps, schema_editor):
    # forwards_func() creates two Country instances,
    # so reverse_func() should delete them.
    Employee = apps.get_model("employees", "employee")
    db_alias = schema_editor.connection.alias
    qs = Employee.objects.using(db_alias).all()
    for i in qs:
        i.user = i.employee_profile
        i.save()


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('employees', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='employees',
                                    to=settings.AUTH_USER_MODEL),
        ),

        migrations.AddField(
            model_name='employee',
            name='employee_profile',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE,
                                    related_name='employeess',
                                    to=settings.AUTH_USER_MODEL),
        ),

        #migrations.RunPython(forwards_func, reverse_func),
    ]

