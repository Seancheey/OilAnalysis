import unittest
from BackEnd import *

test_username = 'random_test'
test_email = 'random_test@test.com'
test_pass = b'abcdabcdabcdabcdabcdabcdabcdabcd'


@contextmanager
def temp_user(username=test_username, email=test_email, password=test_pass):
    try:
        register(username, password, email)
        yield username
    finally:
        with new_session() as session:
            session.query(User).filter(User.username == username).delete()


@contextmanager
def temp_login_session(username=test_username, password=test_pass, expire=30):
    try:
        token = login(username, password, expire_day_len=expire)
        yield token
    finally:
        with new_session() as session:
            session.query(LoginSession).filter(LoginSession.username == username).delete()


@contextmanager
def temp_news():
    try:
        news = OilNews(title='Test Title', publish_date=datetime.today(), author='Qiyi Shan', content='YOLO!',
                       reference='')
        with new_session() as session:
            session.add(news)
    finally:
        with new_session() as session:
            session.query


class MyTestCase(unittest.TestCase):
    def test_register(self):
        with temp_user() as username:
            self.assertEqual(username, test_username)
            try:
                register(test_username, test_pass, 'no_conflict@a.b')
                self.fail()
            except UserAlreadyExistsError:
                pass
            except:
                self.fail()
            try:
                register('no_conflict', test_pass, test_email)
                self.fail()
            except EmailAlreadyExistsError:
                pass
            except:
                self.fail()

    def test_login(self):
        with temp_user() as _:
            with temp_login_session() as _:
                pass
            with temp_login_session(expire=-1) as token:
                with new_session() as s:
                    try:
                        get_login_session(s, token)
                        self.fail()
                    except LoginSessionExpired:
                        pass
                    except:
                        self.fail()

    def test_logout(self):
        with temp_user() as _:
            with temp_login_session() as token:
                logout(token)
                with new_session() as session:
                    self.assertEqual(session.query(LoginSession).filter(LoginSession.session_token == token).count(), 0)

    def test_comment(self):
        pass


if __name__ == '__main__':
    unittest.main()
