from datetime import datetime, timedelta
from typing import Any

from django.contrib.gis.geos import Point

from open_schools_platform.common.filters import SoftCondition
from open_schools_platform.organization_management.circles.models import Circle
from open_schools_platform.organization_management.circles.selectors import get_circles
from open_schools_platform.organization_management.circles.services import create_circle, add_student_to_circle
from open_schools_platform.organization_management.employees.tests.utils import create_test_employee
from open_schools_platform.organization_management.organizations.models import Organization
from open_schools_platform.organization_management.organizations.tests.utils import create_test_organization
from open_schools_platform.organization_management.teachers.models import TeacherProfile
from open_schools_platform.organization_management.teachers.services import create_teacher
from open_schools_platform.parent_management.families.models import Family
from open_schools_platform.query_management.queries.models import Query
from open_schools_platform.query_management.queries.services import create_query
from open_schools_platform.student_management.students.models import Student, StudentProfile
from open_schools_platform.student_management.students.services import create_student
from open_schools_platform.user_management.users.models import User
from open_schools_platform.user_management.users.tests.utils import create_test_user


def create_test_circle(organization: Organization = None, address: str = "address",
                       location: Any = Point(0.0, 0.0), name: str = "test_circle",
                       capacity: int = 10, description: str = "description",
                       start_time: datetime = None, duration: timedelta = None) -> Circle:
    if organization is None:
        organization = create_test_organization()
    circle = create_circle(
        organization=organization,
        name=name,
        address=address,
        capacity=capacity,
        description=description,
        location=location,
        start_time=start_time,
        duration=duration
    )
    return circle


def create_test_circle_with_user_in_org(user: User, organization: Organization = None) -> Circle:
    employee = create_test_employee(user)
    employee.organization = organization or create_test_organization()
    employee.save()
    circle = create_test_circle(employee.organization)
    return circle


def create_student_and_add_to_the_circle(i, circle):
    student = create_student(name=f"test_student{i}")
    add_student_to_circle(student=student, circle=circle)

    return student


def create_data_circle_invite_student(name: str, student_phone: str, parent_phone: str):
    data = {
        "body": {
            "name": name
        },
        "student_phone": student_phone,
        "parent_phone": parent_phone,
        "email": "user@example.com"
    }
    return data


def create_data_circle_invite_teacher(name: str, phone: str):
    data = {
        "body": {
            "name": name
        },
        "phone": phone,
        "email": "user@example.com"
    }
    return data


def create_test_query_circle_invite_student(circle: Circle, family: Family, student: Student,
                                            student_profile: StudentProfile) -> Query:
    query = create_query(sender_model_name="circle", sender_id=circle.id,
                         recipient_model_name="family", recipient_id=family.id,
                         body_model_name="student", body_id=student.id,
                         additional_model_name="studentprofile", additional_id=student_profile.id)
    return query


def create_test_query_circle_invite_teacher(circle: Circle, teacher_profile: TeacherProfile,
                                            name: str = "test_teacher") -> Query:
    teacher = create_teacher(name=name)
    query = create_query(sender_model_name="circle", sender_id=circle.id,
                         recipient_model_name="teacherprofile", recipient_id=teacher_profile.id,
                         body_model_name="teacher", body_id=teacher.id)
    return query


def create_test_teacher_profile(phone: str = "+79998786648"):
    teacher_profile = create_test_user(phone).teacher_profile
    teacher_profile.phone = phone
    teacher_profile.save()
    return teacher_profile


def get_deleted_circles():
    circles = get_circles(filters={'DELETED': SoftCondition.DELETED_ONLY})
    return circles
