# Generated by Django 3.2.12 on 2022-06-08 18:54

from django.db import migrations, models
import django.utils.timezone
import open_schools_platform.user_management.users.models
import phonenumber_field.modelfields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CreationToken',
            fields=[
                ('created_at', models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('key', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(max_length=17, null=True, region=None, verbose_name='telephone number')),
                ('session', models.CharField(max_length=1000, null=True)),
                ('is_verified', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('created_at', models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(max_length=17, null=True, region=None, unique=True, verbose_name='telephone number')),
                ('name', models.CharField(blank=True, max_length=200)),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('jwt_key', models.UUIDField(default=uuid.uuid4)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('objects', open_schools_platform.user_management.users.models.UserManager()),
            ],
        ),
    ]
