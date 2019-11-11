import unittest
from BackEnd import *

test_username = 'random_test'
test_email = 'random_test@test.com'
test_pass = b'abcdabcdabcdabcdabcdabcdabcdabcd'
test_title = 'Test Title'
test_date = datetime.now()


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
        news = OilNews(title=test_title, publish_date=test_date, author='Qiyi Shan', content='YOLO!',
                       reference='')
        with new_session() as session:
            session.add(news)
            session.commit()
            yield session.query(OilNews).filter(OilNews.title == test_title).limit(1).one_or_none()
    finally:
        with new_session() as session:
            session.query(OilNews).filter(OilNews.title == test_title, OilNews.publish_date == test_date).delete()


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

    def test_news(self):
        get_oil_news_list(news_num=5)
        self.assertEqual(len(get_oil_news_list(start_time=datetime.now())), 0)
        with temp_news() as news:
            self.assertEqual(len(get_oil_news_list(news_num=1)), 1)
            self.assertEqual(get_latest_news().title, news.title)

    def test_comment(self):
        pass


if __name__ == '__main__':
    unittest.main()
