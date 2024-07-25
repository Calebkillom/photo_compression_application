#!/usr/bin/python3

import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from os import getenv, environ
from webapp.models import Base, User, Image
from webapp.repositories import ImageRepository, UserRepository

class TestRepositories(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        environ['WEBAPP_MYSQL_USER'] = 'webapp_dev'
        environ['WEBAPP_MYSQL_PWD'] = 'webapp_dev_pwd'
        environ['WEBAPP_MYSQL_HOST'] = 'localhost'
        environ['WEBAPP_MYSQL_DB'] = 'webapp_test_db'
        environ['WEBAPP_ENV'] = 'test'

        cls.engine = create_engine(
            f"mysql+mysqldb://{getenv('WEBAPP_MYSQL_USER')}:{getenv('WEBAPP_MYSQL_PWD')}@{getenv('WEBAPP_MYSQL_HOST')}/{getenv('WEBAPP_MYSQL_DB')}",
            pool_pre_ping=True)
        Base.metadata.create_all(cls.engine)
        cls.Session = scoped_session(sessionmaker(bind=cls.engine))

    @classmethod
    def tearDownClass(cls):
        Base.metadata.drop_all(cls.engine)
        cls.engine.dispose()

    def setUp(self):
        self.session = self.Session()

    def tearDown(self):
        self.session.rollback()
        self.session.close()

    def test_create_user(self):
        user_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'password123'
        }
        user = UserRepository.create_user(self.session, user_data)
        self.assertIsNotNone(user.id)
        self.assertEqual(user.username, 'testuser')

    def test_find_user_by_id(self):
        user_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'password123'
        }
        created_user = UserRepository.create_user(self.session, user_data)
        found_user = UserRepository.find_user_by_id(self.session, created_user.id)
        self.assertEqual(found_user.username, 'testuser')

    def test_find_user_by_username(self):
        user_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'password123'
        }
        UserRepository.create_user(self.session, user_data)
        found_user = UserRepository.find_user_by_username(self.session, 'testuser')
        self.assertEqual(found_user.email, 'testuser@example.com')

    def test_update_user(self):
        user_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'password123'
        }
        created_user = UserRepository.create_user(self.session, user_data)
        update_data = {'email': 'updated@example.com'}
        updated_user = UserRepository.update_user(self.session, created_user.id, update_data)
        self.assertEqual(updated_user.email, 'updated@example.com')

    def test_delete_user(self):
        user_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'password123'
        }
        created_user = UserRepository.create_user(self.session, user_data)
        result = UserRepository.delete_user(self.session, created_user.id)
        self.assertTrue(result)
        deleted_user = UserRepository.find_user_by_id(self.session, created_user.id)
        self.assertIsNone(deleted_user)

    def test_create_image(self):
        user_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'password123'
        }
        user = UserRepository.create_user(self.session, user_data)
        image_data = {
            'file_path': '/home/gammerleb/photo_compression_application/tests/data/image.jpg',
            'original_file_name': 'image.jpg',
            'compressed_file_name': 'image.zst',
            'user_id': user.id
        }
        image = ImageRepository.create_image(self.session, image_data)
        self.assertIsNotNone(image.id)
        self.assertEqual(image.file_path, '/home/gammerleb/photo_compression_application/tests/data/image.jpg')

    def test_get_image_by_id(self):
        user_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'password123'
        }
        user = UserRepository.create_user(self.session, user_data)
        image_data = {
            'file_path': '/home/gammerleb/photo_compression_application/tests/data/image.jpg',
            'original_file_name': 'image.jpg',
            'compressed_file_name': 'image.zst',
            'user_id': user.id
        }
        created_image = ImageRepository.create_image(self.session, image_data)
        found_image = ImageRepository.get_image_by_id(self.session, created_image.id)
        self.assertEqual(found_image.file_path, '/home/gammerleb/photo_compression_application/tests/data/image.jpg')

    def test_get_images_by_user_id(self):
        user_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'password123'
        }
        user = UserRepository.create_user(self.session, user_data)
        image_data = {
            'file_path': '/home/gammerleb/photo_compression_application/tests/data/image.jpg',
            'original_file_name': 'image.jpg',
            'compressed_file_name': 'image.zst',
            'user_id': user.id
        }
        ImageRepository.create_image(self.session, image_data)
        images = ImageRepository.get_images_by_user_id(self.session, user.id)
        self.assertEqual(len(images), 1)
        self.assertEqual(images[0].file_path, '/home/gammerleb/photo_compression_application/tests/data/image.jpg')

    def test_update_image(self):
        user_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'password123'
        }
        user = UserRepository.create_user(self.session, user_data)
        image_data = {
            'file_path': '/home/gammerleb/photo_compression_application/tests/data/image.jpg',
            'original_file_name': 'image.jpg',
            'compressed_file_name': 'image.zst',
            'user_id': user.id
        }
        created_image = ImageRepository.create_image(self.session, image_data)
        update_data = {'file_path': '/home/gammerleb/photo_compression_application/tests/data/new_image.jpg'}
        updated_image = ImageRepository.update_image(self.session, created_image.id, update_data)
        self.assertEqual(updated_image.file_path, '/home/gammerleb/photo_compression_application/tests/data/new_image.jpg')

    def test_delete_image(self):
        user_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'password123'
        }
        user = UserRepository.create_user(self.session, user_data)
        image_data = {
            'file_path': '/home/gammerleb/photo_compression_application/tests/data/image.jpg',
            'original_file_name': 'image.jpg',
            'compressed_file_name': 'image.zst',
            'user_id': user.id
        }
        created_image = ImageRepository.create_image(self.session, image_data)
        result = ImageRepository.delete_image(self.session, created_image.id)
        self.assertTrue(result)
        deleted_image = ImageRepository.get_image_by_id(self.session, created_image.id)
        self.assertIsNone(deleted_image)

    def test_search_images(self):
        user_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'password123'
        }
        user = UserRepository.create_user(self.session, user_data)
        image_data = {
            'file_path': '/home/gammerleb/photo_compression_application/tests/data/image.jpg',
            'original_file_name': 'test_image.jpg',
            'compressed_file_name': 'image.zst',
            'user_id': user.id
        }
        ImageRepository.create_image(self.session, image_data)
        images = ImageRepository.search_images(self.session, user.id, 'test_image')
        self.assertEqual(len(images), 1)
        self.assertEqual(images[0].original_file_name, 'test_image.jpg')

if __name__ == '__main__':
    unittest.main()
