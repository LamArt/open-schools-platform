from open_schools_platform.common.admin import InputFilter, BaseAdmin, admin_wrapper
from open_schools_platform.student_management.students.models import StudentProfile, Student
from django.utils.translation import gettext_lazy as _

from open_schools_platform.student_management.students.selectors import get_students


class CircleFilter(InputFilter):
    parameter_name = 'circle_name'
    title = _('circle name')

    def queryset(self, request, queryset):
        if self.value() is not None:
            circle = self.value()

            return get_students(filters={'circle_name': circle})


class StudentProfileFilter(InputFilter):
    parameter_name = 'student_profile_name'
    title = _('student profile name')

    def queryset(self, request, queryset):
        if self.value() is not None:
            student_profile = self.value()

            return get_students(filters={'student_profile_name': student_profile})


@admin_wrapper(StudentProfile)
class StudentProfileAdmin(BaseAdmin):
    list_display = ('age', 'user', 'id', 'phone')
    search_fields = ('name', 'age', "user__phone", 'phone')


@admin_wrapper(Student)
class StudentAdmin(BaseAdmin):
    list_display = ('student_profile', 'circle', 'id')
    search_fields = ("name",)
    list_filter = (CircleFilter, StudentProfileFilter, StudentProfileFilter)
