import unittest
from flask import session
from flask_testing import TestCase
from ..views.user_repository import UserRepository
from src import db
from src.models.system_user_model import SystemUser


class TestUserRepository(TestCase):

    def setUp(self) -> None:
        session["username"] = "username"
        db.create_all()

    def test_query_system_user(self):
        user_email = "test@test.com"
        user = SystemUser(email=user_email)
        db.session.add(user)
        db.session.commit()

        result = UserRepository.query_system_user(user_email)
        self.assertEqual(result.email, "test@test.com")

    def tearDown(self) -> None:
        db.drop_all()
