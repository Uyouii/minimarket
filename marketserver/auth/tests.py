from django.test import TestCase
import auth
from common import conf


# Create your tests here.
class AuthTests(TestCase):

    def test_check_user_right_session(self):
        user_id = 1497239843518041
        session = 'b4f26e61b129a02fa6b5a223'
        res = auth.checkUserSession(user_id, session)
        self.assertEqual(res, 0)

    def test_check_user_wrong_session(self):
        user_id = 522844585160240
        session = '12345'
        res = auth.checkUserSession(user_id, session)
        self.assertEqual(res, conf.ERR_WROING_SESSION)

    def test_check_not_register_user(self):
        user_id = 100
        session = '12345'
        res = auth.checkUserSession(user_id, session)
        self.assertEqual(res, conf.ERR_USER_NOT_RESISTER)
