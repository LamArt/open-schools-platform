# Generated by Django 3.2.12 on 2023-01-02 20:25

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.utils.timezone
import phonenumber_field.modelfields
import rules.contrib.models
import simple_history.models
import uuid

from safedelete.config import DELETED_VISIBLE


def create_teacher_profile_for_user(apps, schema_editor):
    TeacherProfile = apps.get_model("teachers", "teacherprofile")
    User = apps.get_model("users", "user")
    db_alias = schema_editor.connection.alias
    qs = User.objects.using(db_alias).all(force_visibility=DELETED_VISIBLE)
    for user in qs:
        teacher_profile = TeacherProfile()
        teacher_profile.name = 'teacher'
        teacher_profile.user = user
        teacher_profile.phone = user.phone
        teacher_profile.save(using=db_alias)


def delete_teacher_profile(apps, schema_editor):
    TeacherProfile = apps.get_model("teachers", "teacherprofile")
    db_alias = schema_editor.connection.alias
    TeacherProfile.objects.using(db_alias).all().delete()


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('photos', '0001_initial_squashed_0004_refactoring_history'),
        ('circles', '0005_auto_20221029_1535_squashed_0006_added_history_records'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TeacherProfile',
            fields=[
                ('deleted', models.DateTimeField(db_index=True, editable=False, null=True)),
                ('deleted_by_cascade', models.BooleanField(default=False, editable=False)),
                ('created_at', models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('age',
                 models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)])),
                ('phone',
                 phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=17, null=True, region=None,
                                                                verbose_name='telephone number')),
                ('photo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL,
                                            to='photos.photo')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                              related_name='teacher_profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(rules.contrib.models.RulesModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('deleted', models.DateTimeField(db_index=True, editable=False, null=True)),
                ('deleted_by_cascade', models.BooleanField(default=False, editable=False)),
                ('created_at', models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('circle', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                             related_name='teachers', to='circles.circle')),
                ('teacher_profile',
                 models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                   related_name='teachers', to='teachers.teacherprofile')),
            ],
            options={
                'abstract': False,
            },
            bases=(rules.contrib.models.RulesModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalTeacherProfile',
            fields=[
                ('deleted', models.DateTimeField(db_index=True, editable=False, null=True)),
                ('deleted_by_cascade', models.BooleanField(default=False, editable=False)),
                ('created_at', models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(blank=True, editable=False)),
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4)),
                ('name', models.CharField(max_length=200)),
                ('age',
                 models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)])),
                ('phone',
                 phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=17, null=True, region=None,
                                                                verbose_name='telephone number')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type',
                 models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user',
                 models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+',
                                   to=settings.AUTH_USER_MODEL)),
                ('photo', models.ForeignKey(blank=True, db_constraint=False, null=True,
                                            on_delete=django.db.models.deletion.DO_NOTHING, related_name='+',
                                            to='photos.photo')),
                ('user', models.ForeignKey(blank=True, db_constraint=False, null=True,
                                           on_delete=django.db.models.deletion.DO_NOTHING, related_name='+',
                                           to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical teacher profile',
                'verbose_name_plural': 'historical teacher profiles',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalTeacher',
            fields=[
                ('deleted', models.DateTimeField(db_index=True, editable=False, null=True)),
                ('deleted_by_cascade', models.BooleanField(default=False, editable=False)),
                ('created_at', models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(blank=True, editable=False)),
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4)),
                ('name', models.CharField(max_length=200)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type',
                 models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('circle', models.ForeignKey(blank=True, db_constraint=False, null=True,
                                             on_delete=django.db.models.deletion.DO_NOTHING, related_name='+',
                                             to='circles.circle')),
                ('history_user',
                 models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+',
                                   to=settings.AUTH_USER_MODEL)),
                ('teacher_profile', models.ForeignKey(blank=True, db_constraint=False, null=True,
                                                      on_delete=django.db.models.deletion.DO_NOTHING, related_name='+',
                                                      to='teachers.teacherprofile')),
            ],
            options={
                'verbose_name': 'historical teacher',
                'verbose_name_plural': 'historical teachers',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.RunPython(create_teacher_profile_for_user, delete_teacher_profile)
    ]