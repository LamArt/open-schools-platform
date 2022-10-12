import uuid

from django.core.validators import MinValueValidator
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from phonenumber_field.phonenumber import PhoneNumber

from open_schools_platform.common.models import BaseModel
from open_schools_platform.photo_management.photos.models import Photo
from open_schools_platform.user_management.users.models import User
from open_schools_platform.organization_management.circles.models import Circle


class StudentProfileManager(models.Manager):
    def create_student_profile(
            self, name: str, age: int = 0, phone: PhoneNumber = None, user: User = None, photo: uuid = None):
        student_profile = self.model(
            name=name,
            age=age,
            user=user,
            phone=phone,
            photo=photo
        )
        student_profile.full_clean()
        student_profile.save(using=self.db)
        return student_profile


class StudentProfile(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile', null=True, blank=True)
    name = models.CharField(max_length=200)
    age = models.IntegerField(validators=[MinValueValidator(0)])
    phone = PhoneNumberField(
        verbose_name='telephone number',
        max_length=17,
        blank=True,
        null=True,
    )
    photo = models.ForeignKey(Photo, on_delete=models.SET_NULL, null=True, related_name="photo", blank=True)

    objects = StudentProfileManager()

    def __str__(self):
        return self.name.__str__()


class StudentManager(models.Manager):
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
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=200)
    circle = models.ForeignKey(Circle, on_delete=models.CASCADE, null=True, related_name="students", blank=True)
    student_profile = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, null=True, related_name="students",
                                        blank=True)
    objects = StudentManager()

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
