# Generated by Django 3.2.12 on 2022-10-23 14:50

from django.db import migrations, models
import django.db.models.deletion


def photo_field_to_temp_table(apps, schema_editor):
    PhotoTemp = apps.get_model("students", "phototemp")
    StudentProfile = apps.get_model("students", "studentprofile")
    db_alias = schema_editor.connection.alias
    qs = StudentProfile.objects.using(db_alias).filter(photo__isnull=False).all()
    for student_profile in qs:
        photo_temp = PhotoTemp()
        photo_temp.image = student_profile.photo
        photo_temp.student_profile = student_profile.id
        photo_temp.save(using=db_alias)
    schema_editor.execute(f"update {StudentProfile._meta.db_table} set photo = null")


def reverse_fill_photo_field_from_temp_table(apps, schema_editor):
    StudentProfile = apps.get_model("students", "studentprofile")
    PhotoTemp = apps.get_model("students", "phototemp")
    db_alias = schema_editor.connection.alias
    qs = PhotoTemp.objects.using(db_alias).all()
    for photo_temp in qs:
        student_profile = StudentProfile.objects.using(db_alias).get(id=photo_temp.student_profile)
        student_profile.photo = photo_temp.image
        student_profile.save(using=db_alias)


def fill_photo_model_from_temp_table(apps, schema_editor):
    StudentProfile = apps.get_model("students", "studentprofile")
    PhotoTemp = apps.get_model("students", "phototemp")
    Photo = apps.get_model("photos", "photo")
    db_alias = schema_editor.connection.alias
    qs = PhotoTemp.objects.using(db_alias).all()
    for photo_temp in qs:
        student_profile = StudentProfile.objects.using(db_alias).get(id=photo_temp.student_profile)
        photo = Photo()
        photo.image = photo_temp.image
        photo.save(using=db_alias)
        student_profile.photo = photo
        student_profile.save(using=db_alias)


def reverse_photo_model_to_temp_table(apps, schema_editor):
    StudentProfile = apps.get_model("students", "studentprofile")
    PhotoTemp = apps.get_model("students", "phototemp")
    db_alias = schema_editor.connection.alias
    qs = StudentProfile.objects.using(db_alias).filter(photo__isnull=False).all()
    for student_profile in qs:
        photo_temp = PhotoTemp()
        photo_temp.image = student_profile.photo.image
        photo_temp.student_profile = student_profile.id
        photo_temp.save(using=db_alias)


def create_photo_if_null(apps, schema_editor):
    Photo = apps.get_model("photos", "photo")
    StudentProfile = apps.get_model("students", "studentprofile")
    db_alias = schema_editor.connection.alias
    qs = StudentProfile.objects.using(db_alias).filter(photo__isnull=True).all()
    for student_profile in qs:
        photo = Photo()
        photo.save(using=db_alias)
        student_profile.photo = photo
        student_profile.save(using=db_alias)


def delete_photo(apps, schema_editor):
    Photo = apps.get_model("photos", "photo")
    db_alias = schema_editor.connection.alias
    Photo.objects.using(db_alias).all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ('photos', '0001_initial'),
        ('students', '0003_studentprofile_photo'),
    ]

    operations = [
        migrations.CreateModel(
            name='PhotoTemp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.CharField(max_length=100)),
                ('student_profile', models.UUIDField(blank=True, null=True)),
            ],
        ),
        migrations.RunPython(photo_field_to_temp_table, reverse_fill_photo_field_from_temp_table),


        migrations.AlterField(
            model_name='studentprofile',
            name='photo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL,
                                    related_name='photo', to='photos.photo'),
        ),
        migrations.RunPython(create_photo_if_null, delete_photo),
        migrations.RunPython(fill_photo_model_from_temp_table, reverse_photo_model_to_temp_table),
        migrations.DeleteModel('phototemp')
    ]
