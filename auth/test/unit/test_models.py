import unittest

from flask_migrate import upgrade

from app import create_app
from app.extensions import SQL_DB
from app.models import User, Token


class TestUserModel(unittest.TestCase):
    def setUp(self):
        self.app = create_app('config.TestConfig')
        self.app_ctxt = self.app.app_context()
        self.app_ctxt.push()
        upgrade()
        self.user = User(id='1', email='test@example.com', password_hash='hashedpassword')
        SQL_DB.session.add(self.user)
        SQL_DB.session.commit()

    def tearDown(self):
        SQL_DB.session.remove()
        self.app_ctxt.pop()
        self.app = None
        self.app_ctxt = None

    def test_user_model(self):
        u = User.query.get(1)
        self.assertEqual(u.email, 'test@example.com')
        self.assertEqual(u.password_hash, 'hashedpassword')

    def test_token_model(self):
        token = Token(id='1', jti='jti', token_type='access', user_identity='1', expires=9999999999, revoked=False)
        SQL_DB.session.add(token)
        SQL_DB.session.commit()

        t = Token.query.get(1)
        self.assertEqual(t.jti, 'jti')
        self.assertEqual(t.token_type, 'access')
        self.assertEqual(t.user_identity, '1')
        self.assertEqual(t.expires, 9999999999)
        self.assertEqual(t.revoked, False)


if __name__ == "__main__":
    unittest.main()