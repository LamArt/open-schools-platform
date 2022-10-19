from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from open_schools_platform.user_management.users.tests.utils import create_logged_in_user


class PhotoTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.query_photo_update_url = lambda pk: reverse("api:photo-management:photos:create-photo", args=[pk])

    def test_update_new_user_photo(self):
        user = create_logged_in_user(self)
        response = self.client.put(self.query_photo_update_url(user.student_profile.photo.id))
        self.assertEqual(200, response.status_code)
