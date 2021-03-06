import datetime
import pytz
from django.test import TestCase
from rest_framework_jwt.utils import jwt_decode_token
from rest_framework import serializers

from open_schools_platform.user_management.users.services import create_token, is_token_alive, verify_token, \
    create_user, user_update, get_jwt_token, update_token_session, generate_user_password, set_new_password_for_user


class IsTokenAliveTests(TestCase):
    def test_token_with_old_date_of_creation_is_not_alive(self):
        token = create_token(
            phone="+79020000000",
            session="000000"
        )
        token.created_at = datetime.datetime(2000, 9, 19, 10, 40, 23, 944737, tzinfo=pytz.UTC)
        token.save()
        result = is_token_alive(token)
        self.assertFalse(result)

    def test_token_with_recent_date_of_creation_is_alive(self):
        token = create_token(
            phone="+79020000000",
            session="000000"
        )
        token.created_at = datetime.datetime(2023, 9, 19, 10, 40, 23, 944737, tzinfo=pytz.UTC)
        token.save()
        result = is_token_alive(token)
        self.assertTrue(result)


class TokenCreateTests(TestCase):
    def test_user_without_phone_number_cannot_be_created(self):
        self.assertRaises(ValueError, lambda: create_token(phone="", session="000000"))


class UserUpdateTests(TestCase):
    def test_user_with_valid_data_can_be_updated(self):
        user = create_user(phone="+79022222222", password="123456", name="Alex")
        data_for_user_update = {
            "name": "Schwarz"
        }
        user_update(user=user, data=data_for_user_update)
        self.assertEqual(user.name, "Schwarz")


class VerifyTokenTests(TestCase):
    def test_successfully_token_verify(self):
        token = create_token(
            phone="+79020000000",
            session="000000"
        )
        verify_token(token)
        self.assertTrue(token.is_verified)


class GetJwtTokenTests(TestCase):
    def test_successfully_get_jwt_token(self):
        user = create_user(
            phone="+79020000000",
            password="123456",
            name="Alex"
        )
        user_password = "123456"
        jwt_token = get_jwt_token(user.USERNAME_FIELD, str(user.get_username()), user_password, request=None)
        data_from_jwt = jwt_decode_token(jwt_token)
        self.assertEqual(user.phone, data_from_jwt["username"])

    def test_user_does_not_exist(self):
        self.assertRaises(serializers.ValidationError,
                          lambda: get_jwt_token("+79020000000", "+79020000000", "123456", request=None))


class UpdateTokenSessionTests(TestCase):
    def test_successfully_update_token_session(self):
        token = create_token(
            phone="+79020000000",
            session="000000"
        )
        update_token_session(token, "111111")
        self.assertEqual("111111", token.session)


class GenerateUserPassword(TestCase):
    def test_successfully_generate_password_for_user(self):
        credentials = {
            "phone": "+79020000000",
            "password": "123456",
            "name": "test_user"
        }

        create_user(**credentials)
        new_user_password = generate_user_password()
        self.assertNotEqual(credentials["password"], new_user_password)


class SetNewPasswordForUserTests(TestCase):
    def test_successfully_set_new_password_for_user(self):
        credentials = {
            "phone": "+79020000000",
            "password": "123456",
            "name": "test_user"
        }

        user = create_user(**credentials)
        set_new_password_for_user(user, "654321")
        result = user.check_password("654321")
        self.assertTrue(result)
