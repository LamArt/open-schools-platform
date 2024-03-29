from django.core.validators import MinValueValidator
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers

from open_schools_platform.common.serializers import BaseModelSerializer
from open_schools_platform.photo_management.photos.serializers import GetPhotoSerializer
from open_schools_platform.shared.serializers import GetShallowCircleSerializer
from open_schools_platform.student_management.students.models import StudentProfile, Student, \
    StudentProfileCircleAdditional


class CreateStudentProfileAutoStudentJoinCircleSerializer(BaseModelSerializer):

    class Meta:
        model = StudentProfile
        fields = ("age", "name", "phone")


class UpdateStudentProfileSerializer(serializers.Serializer):
    family = serializers.UUIDField(default=None, required=False)
    name = serializers.CharField(max_length=200, required=False, default=None)
    age = serializers.IntegerField(validators=[MinValueValidator(0)], required=False, default=None)
    phone = PhoneNumberField(max_length=17, required=False)


class GetStudentProfileSerializer(BaseModelSerializer):
    photo = GetPhotoSerializer()
    parent_phones = serializers.SerializerMethodField('get_parent_phones')
    parent_names = serializers.SerializerMethodField('get_parent_names')

    def get_parent_phones(self, obj):
        families = obj.families.prefetch_related('parent_profiles').all()
        return ",".join([str(j.user.phone) for i in families for j in i.parent_profiles.all()])

    def get_parent_names(self, obj):
        families = obj.families.prefetch_related('parent_profiles').all()
        return ",".join([str(j.name) for i in families for j in i.parent_profiles.all()])

    class Meta:
        model = StudentProfile
        fields = ("id", "name", "age", "phone", "photo", "parent_phones", "parent_names")


class CreateStudentProfileSerializer(BaseModelSerializer):
    family = serializers.UUIDField(required=True)

    class Meta:
        model = StudentProfile
        fields = ("name", "age", "phone", "family")


class GetStudentProfileSenderForOrganizationSerializer(BaseModelSerializer):
    photo = GetPhotoSerializer()

    class Meta:
        model = StudentProfile
        fields = ("id", "photo")


class GetStudentBodySerializer(BaseModelSerializer):

    class Meta:
        model = Student
        fields = ("id", "name")


class CreateStudentBodySerializer(BaseModelSerializer):

    class Meta:
        model = Student
        fields = ("name", )


class GetStudentSerializer(BaseModelSerializer):
    student_profile = GetStudentProfileSerializer()
    circle = GetShallowCircleSerializer()

    class Meta:
        model = Student
        fields = ("id", "name", "circle", "student_profile")


class GetStudentJoinCircleContext(BaseModelSerializer):
    class Meta:
        model = StudentProfileCircleAdditional
        fields = ("parent_phone", "parent_name", "student_phone", "text")


class GetCircleInviteStudentContext(BaseModelSerializer):
    class Meta:
        model = StudentProfile
        fields = ("id", "name", "phone")


class CreateStudentJoinCircleContext(BaseModelSerializer):
    class Meta:
        model = StudentProfileCircleAdditional
        fields = ("text", )


class CreateAutoStudentJoinCircleSerializer(serializers.Serializer):
    circle = serializers.UUIDField(required=True)
    additional = CreateStudentJoinCircleContext()
    student_profile = CreateStudentProfileAutoStudentJoinCircleSerializer()


class CreateStudentJoinCircleSerializer(serializers.Serializer):
    circle = serializers.UUIDField(required=True)
    additional = CreateStudentJoinCircleContext()


class UpdateStudentJoinCircleSerializer(serializers.Serializer):
    query = serializers.UUIDField(required=True)
    body = CreateStudentBodySerializer()


class UpdateStudentSerializer(BaseModelSerializer):
    class Meta:
        model = Student
        fields = ("name", )
