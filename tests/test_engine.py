import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from os import getenv, environ
from webapp.engine.storage_engine import DBStorage
from webapp.models import Base, User, Image
from webapp.engine import get_session

class TestDBStorage(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        environ['WEBAPP_MYSQL_USER'] = 'webapp_dev'
        environ['WEBAPP_MYSQL_PWD'] = 'webapp_dev_pwd'
        environ['WEBAPP_MYSQL_HOST'] = 'localhost'
        environ['WEBAPP_MYSQL_DB'] = 'webapp_test_db'
        environ['WEBAPP_ENV'] = 'test'

        cls.storage = DBStorage()
        cls.storage.reload()

    @classmethod
    def tearDownClass(cls):
        cls.storage._DBStorage__session.remove()
        Base.metadata.drop_all(cls.storage._DBStorage__engine)

    def setUp(self):
        self.session = self.storage._DBStorage__session()

    def tearDown(self):
        self.session.rollback()
        self.session.close()

    def test_engine_initialization(self):
        self.assertIsNotNone(self.storage._DBStorage__engine)

    def test_session_initialization(self):
        self.assertIsNotNone(self.storage._DBStorage__session)

    def test_all_method(self):
        users = self.storage.all(User)
        self.assertEqual(users, {})

        images = self.storage.all(Image)
        self.assertEqual(images, {})

    def test_new_method(self):
        new_user = User(username='testuser', email='testuser@example.com', password='password123')
        self.storage.new(new_user)
        self.storage.save()

        saved_user = self.session.query(User).filter_by(username='testuser').first()
        self.assertIsNotNone(saved_user)
        self.assertEqual(saved_user.username, 'testuser')

    def test_delete_method(self):
        new_user = User(username='testuser', email='testuser@example.com', password='password123')
        self.storage.new(new_user)
        self.storage.save()

        saved_user = self.session.query(User).filter_by(username='testuser').first()
        self.storage.delete(saved_user)
        self.storage.save()

        deleted_user = self.session.query(User).filter_by(username='testuser').first()
        self.assertIsNone(deleted_user)

    def test_reload_method(self):
        self.storage.reload()
        self.assertIsNotNone(self.storage._DBStorage__session)

if __name__ == '__main__':
    unittest.main()