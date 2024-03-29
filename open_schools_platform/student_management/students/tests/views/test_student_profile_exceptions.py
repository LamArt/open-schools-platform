import uuid

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from open_schools_platform.organization_management.circles.tests.utils import create_test_circle
from open_schools_platform.parent_management.families.services import create_family, \
    add_student_profile_to_family, add_parent_profile_to_family
from open_schools_platform.student_management.students.services import create_student_profile
from open_schools_platform.user_management.users.tests.utils import create_logged_in_user, create_test_user


class StudentProfileExceptionsTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.student_profile_url = reverse("api:students-management:students:create-student-profile")
        self.student_profile_edit_url = lambda pk: \
            reverse("api:students-management:students:student-profile", args=[pk])
        self.student_join_circle_query_url = reverse("api:students-management:students:auto-student-join-circle-query")

    def test_family_does_not_exist(self):
        user = create_logged_in_user(instance=self)
        student_profile_create_data = {
            "age": 15,
            "name": "test_student_profile",
            "family": "99999999-9999-9999-9999-999999999999",
        }
        student_profile_create_response = self.client.post(self.student_profile_url,
                                                           student_profile_create_data)
        self.assertEqual(404, student_profile_create_response.status_code)

        student_profile = create_student_profile(name="test_name", age=15)
        family = create_family(user.parent_profile, "Simpsons")
        add_parent_profile_to_family(family=family, parent=user.parent_profile)
        add_student_profile_to_family(family=family, student_profile=student_profile)

        student_profile_update_data = {
            "family": "99999999-9999-9999-9999-999999999999",
            "age": 15,
            "name": "test_student_profile"
        }
        student_profile_update_response = self.client.patch(self.student_profile_edit_url(student_profile.id),
                                                            student_profile_update_data)
        self.assertEqual(404, student_profile_update_response.status_code)

    def test_current_user_cannot_interact_with_student_profile(self):
        create_logged_in_user(instance=self)
        user = create_test_user(phone="+79020000000")
        family = create_family(name="test_family", parent=user.parent_profile)
        student_profile_create_data = {
            "age": 15,
            "name": "test_student_profile",
            "family": family.id,
        }
        student_profile_create_response = self.client.post(self.student_profile_url,
                                                           student_profile_create_data)
        self.assertEqual(403, student_profile_create_response.status_code)

        student_profile = create_student_profile(name="test_name", age=15)
        student_profile_update_with_family_data = {
            "family": family.id,
            "age": 15,
            "name": "test_name"
        }
        student_profile_update_with_family_response = self.client.patch(
            self.student_profile_edit_url(student_profile.id), student_profile_update_with_family_data)
        self.assertEqual(403, student_profile_update_with_family_response.status_code)

        student_profile_update_data = {
            "age": 15,
            "name": "test_name"
        }
        student_profile_update_response = self.client.patch(self.student_profile_edit_url(student_profile.id),
                                                            student_profile_update_data)
        self.assertEqual(403, student_profile_update_response.status_code)

    def test_student_profile_does_not_exist(self):
        create_logged_in_user(instance=self)
        student_profile_update_data = {
            "age": 15,
            "name": "test_name"
        }
        student_profile_update_response = self.client.patch(
            self.student_profile_edit_url("99999999-9999-9999-9999-999999999999"), student_profile_update_data)
        self.assertEqual(404, student_profile_update_response.status_code)

    def test_family_already_exists(self):
        user = create_logged_in_user(instance=self)
        create_family(name="test_family", parent=user.parent_profile)
        circle = create_test_circle()
        student_join_circle_query_data = {
            "student_profile": {
                "name": "test_name",
                "age": 15,
            },
            "additional": {
                "text": "Please, let me in!",
            },
            "circle": circle.id,
        }
        student_join_circle_query_response = self.client.post(self.student_join_circle_query_url,
                                                              student_join_circle_query_data, format="json")
        self.assertEqual(400, student_join_circle_query_response.status_code)

    def test_delete_student_profile_does_not_exist(self):
        create_logged_in_user(self)
        response = self.client.delete(self.student_profile_edit_url(uuid.uuid4()))
        self.assertEqual(404, response.status_code)

    def test_student_profile_delete_wrong_access(self):
        create_logged_in_user(self)
        student_profile = create_test_user("+79992337714").student_profile
        response = self.client.delete(self.student_profile_edit_url(student_profile.id))
        self.assertEqual(403, response.status_code)
