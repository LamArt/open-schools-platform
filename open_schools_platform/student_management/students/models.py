from typing import Optional, Union, Tuple, Type, Any  # noqa: F401

from safedelete.queryset import SafeDeleteQueryset  # noqa: F401
import uuid

import safedelete
from django.core.validators import MinValueValidator
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from phonenumber_field.phonenumber import PhoneNumber
from simple_history.models import HistoricalRecords

from open_schools_platform.common.models import BaseModel, BaseManager
from open_schools_platform.errors.exceptions import AlreadyExists
from open_schools_platform.photo_management.photos.models import Photo
from open_schools_platform.user_management.users.models import User
from open_schools_platform.organization_management.circles.models import Circle


class StudentProfileManager(BaseManager):
    def create_student_profile(self, name: str, age: int = None, phone: PhoneNumber = None, user: User = None,
                               photo: uuid.UUID = None):
        if not photo:
            photo = Photo.objects.create_photo()

        if not user:
            return self.create(name=name, age=age, phone=phone, photo=photo, user=user)

        try:
            student_profile = self.get(user=user)
        except StudentProfile.DoesNotExist:
            student_profile = None
        if student_profile and not student_profile.deleted:
            raise AlreadyExists("StudentProfile with this user already exists")

        student_profile = self.update_or_create_with_check(user=user,
                                                           defaults={'name': name, 'age': age, 'phone': phone,
                                                                     'photo': photo})
        return student_profile


class StudentProfile(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile', null=True, blank=True)
    name = models.CharField(max_length=200)
    age = models.IntegerField(validators=[MinValueValidator(0)], blank=True, null=True)
    phone = PhoneNumberField(
        verbose_name='telephone number',
        max_length=17,
        blank=True,
        null=True,
    )
    photo = models.ForeignKey(Photo, on_delete=models.SET_NULL, null=True, blank=True, related_name="student_profile")
    history = HistoricalRecords()

    objects = StudentProfileManager()  # type: ignore[assignment]

    def __str__(self):
        return self.name.__str__()


class StudentManager(BaseManager):
    def create_student(self, name: str, circle: Circle = None, student_profile: StudentProfile = None):
        student = self.model(
            name=name,
            circle=circle,
            student_profile=student_profile
        )
        student.full_clean()
        student.save(using=self.db)
        return student


class Student(BaseModel):
    _safedelete_policy = safedelete.config.SOFT_DELETE_CASCADE
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=200)
    circle = models.ForeignKey(Circle, on_delete=models.CASCADE, null=True, related_name="students", blank=True)
    student_profile = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, null=True, related_name="students",
                                        blank=True)

    objects = StudentManager()  # type: ignore[assignment]
    history = HistoricalRecords()

    def __str__(self):
        return self.name


class StudentProfileCircleAdditional(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    student_phone = PhoneNumberField(
        verbose_name='telephone number',
        max_length=17,
        blank=True,
        default="",
        null=True,
    )
    parent_phone = PhoneNumberField(
        verbose_name='telephone number',
        max_length=17,
        blank=True,
        default="",
        null=True,
    )
    parent_name = models.CharField(max_length=255, blank=True, default="", null=True)
    text = models.CharField(max_length=255, blank=True, default="", null=True)
