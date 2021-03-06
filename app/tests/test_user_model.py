import unittest

import datetime

from app.main import db
from app.main.models.user import User
from app.tests.base import BaseTestCase


class TestUserModel(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.user = User(
            email='test@test.com',
            password='test',
            registered_on=datetime.datetime.utcnow()
        )
        db.session.add(self.user)
        db.session.commit()

    def test_encode_auth_token(self):
        auth_token = User.encode_auth_token(self.user.id)
        self.assertTrue(isinstance(auth_token, bytes))

    def test_decode_auth_token(self):
        auth_token = User.encode_auth_token(self.user.id)
        self.assertTrue(isinstance(auth_token, bytes))
        self.assertTrue(User.decode_auth_token(auth_token.decode("utf-8")) == 1)


if __name__ == '__main__':
    unittest.main()

