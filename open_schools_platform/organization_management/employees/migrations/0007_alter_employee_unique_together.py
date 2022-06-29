# Generated by Django 3.2.3 on 2022-06-29 09:12

from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0006_change_relations'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='employee',
            unique_together=("organization", "employee_profile"),
        ),
        migrations.RemoveField(
            model_name='employee',
            name='user',
        ),

        migrations.AlterField(
            model_name='employee',
            name='employee_profile',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='employees',
                                    to='employees.employeeprofile'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='employeeprofile',
            name='user',
            field=models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE,
                                       related_name='employee_profile', to='users.user'),
            preserve_default=False,
        ),
    ]