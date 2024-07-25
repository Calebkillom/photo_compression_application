#!/usr/bin/python3
import unittest
from unittest.mock import patch, MagicMock
from webapp.services.image_service import ImageService
from webapp.services.user_service import UserService
from webapp.models import Image, User
from webapp.repositories import ImageRepository, UserRepository
from webapp.engine import get_session

class TestImageService(unittest.TestCase):

    @patch('webapp.engine.get_session')
    def test_upload_image(self, mock_get_session):
        session = MagicMock()
        mock_get_session.return_value = session
        user = User(username='testuser', password='password123', email='testuser@example.com')
        session.query(User).filter_by(id=1).first.return_value = user

        file_path = '/home/gammerleb/photo_compression_application/tests/data/image.jpg'
        original_file_name = 'image.jpg'
        compressed_file_name = 'image.zst'
        user_id = 1

        with patch.object(ImageRepository, 'create_image') as mock_create_image:
            image_dict = ImageService.upload_image(file_path, original_file_name, compressed_file_name, user_id)
            mock_create_image.assert_called_once()
            self.assertEqual(image_dict['file_path'], file_path)

    @patch('webapp.engine.get_session')
    def test_compress_image(self, mock_get_session):
        session = MagicMock()
        mock_get_session.return_value = session
        image = Image(file_path='/home/gammerleb/photo_compression_application/tests/data/image.jpg',
                      original_file_name='image.jpg', user_id=1)
        session.query(Image).filter_by(id=1).first.return_value = image

        with patch('webapp.services.image_service.zstd.ZstdCompressor') as mock_compressor:
            mock_compressor.return_value.compress.return_value = b'compressed data'
            image_dict = ImageService.compress_image(1, 3)
            self.assertEqual(image_dict['compressed_file_name'], '/home/gammerleb/photo_compression_application/tests/data/image.jpg.zst')

    @patch('webapp.engine.get_session')
    def test_decompress_image(self, mock_get_session):
        session = MagicMock()
        mock_get_session.return_value = session
        image = Image(file_path='/home/gammerleb/photo_compression_application/tests/data/image.jpg.zst',
                      original_file_name='image.jpg', user_id=1, compressed_file_name='/home/gammerleb/photo_compression_application/tests/data/image.jpg.zst')
        session.query(Image).filter_by(id=1).first.return_value = image

        with patch('webapp.services.image_service.zstd.ZstdDecompressor') as mock_decompressor:
            mock_decompressor.return_value.decompress.return_value = b'decompressed data'
            image_dict = ImageService.decompress_image(1)
            self.assertEqual(image_dict['file_path'], '/home/gammerleb/photo_compression_application/tests/data/image.jpg')

    @patch('webapp.engine.get_session')
    def test_delete_image(self, mock_get_session):
        session = MagicMock()
        mock_get_session.return_value = session
        image = Image(file_path='/home/gammerleb/photo_compression_application/tests/data/image.jpg',
                      original_file_name='image.jpg', user_id=1)
        session.query(Image).filter_by(id=1).first.return_value = image

        with patch.object(ImageRepository, 'delete_image') as mock_delete_image:
            result = ImageService.delete_image(1)
            mock_delete_image.assert_called_once_with(session, 1)
            self.assertTrue(result)

    @patch('webapp.engine.get_session')
    def test_search_images(self, mock_get_session):
        session = MagicMock()
        mock_get_session.return_value = session
        image = Image(file_path='/home/gammerleb/photo_compression_application/tests/data/image.jpg',
                      original_file_name='test_image.jpg', user_id=1)

        with patch.object(ImageRepository, 'search_images') as mock_search_images:
            mock_search_images.return_value = [image]
            images = ImageService.search_images(1, 'test_image')
            self.assertEqual(len(images), 1)
            self.assertEqual(images[0]['original_file_name'], 'test_image.jpg')


class TestUserService(unittest.TestCase):

    @patch('webapp.engine.get_session')
    def test_register_user(self, mock_get_session):
        session = MagicMock()
        mock_get_session.return_value = session

        username = 'testuser'
        password = 'password123'
        email = 'testuser@example.com'
        firstname = 'Test'
        lastname = 'User'

        with patch.object(UserRepository, 'create_user') as mock_create_user:
            user_dict = UserService.register_user(username, password, email, firstname, lastname)
            mock_create_user.assert_called_once()
            self.assertEqual(user_dict['username'], username)

    @patch('webapp.engine.get_session')
    def test_authenticate_user(self, mock_get_session):
        session = MagicMock()
        mock_get_session.return_value = session
        user = User(username='testuser', password='password123', email='testuser@example.com')
        session.query(User).filter_by(username='testuser').first.return_value = user

        with patch.object(UserRepository, 'find_user_by_username') as mock_find_user:
            mock_find_user.return_value = user
            user_dict = UserService.authenticate_user('testuser', 'password123')
            mock_find_user.assert_called_once_with(session, 'testuser')
            self.assertEqual(user_dict['username'], 'testuser')

    @patch('webapp.engine.get_session')
    def test_update_user_profile(self, mock_get_session):
        session = MagicMock()
        mock_get_session.return_value = session
        user = User(username='testuser', password='password123', email='testuser@example.com', first_name='Test', last_name='User')
        session.query(User).filter_by(id=1).first.return_value = user

        with patch.object(UserRepository, 'update_user') as mock_update_user:
            user_dict = UserService.update_user_profile(1, 'Updated', 'Name')
            mock_update_user.assert_called_once()
            self.assertEqual(user_dict['first_name'], 'Updated')
            self.assertEqual(user_dict['last_name'], 'Name')

    @patch('webapp.engine.get_session')
    def test_delete_user(self, mock_get_session):
        session = MagicMock()
        mock_get_session.return_value = session
        user = User(username='testuser', password='password123', email='testuser@example.com')
        session.query(User).filter_by(id=1).first.return_value = user

        with patch.object(UserRepository, 'delete_user') as mock_delete_user:
            result = UserService.delete_user(1)
            mock_delete_user.assert_called_once_with(session, 1)
            self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
