#!/usr/bin/python3
import unittest
from webapp.models.base_model import BaseModel, Base
from webapp.models.user import User
from webapp.models.image import Image
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

class TestBaseModel(unittest.TestCase):
    def setUp(self):
        # Create an in-memory SQLite database for testing
        engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(engine)
        self.Session = sessionmaker(bind=engine)
        self.session = self.Session()

    def tearDown(self):
        self.session.close()

    def test_instance_creation(self):
        base = BaseModel()
        self.assertIsInstance(base, BaseModel)
        self.assertIsNotNone(base.id)
        self.assertIsNotNone(base.created_at)
        self.assertIsNotNone(base.updated_at)

    def test_to_dict(self):
        base = BaseModel()
        base_dict = base.to_dict()
        self.assertEqual(base_dict["__class__"], "BaseModel")
        self.assertEqual(base_dict["id"], base.id)
        self.assertEqual(base_dict["created_at"], base.created_at.isoformat())
        self.assertEqual(base_dict["updated_at"], base.updated_at.isoformat())

class TestUserModel(unittest.TestCase):
    def setUp(self):
        engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(engine)
        self.Session = sessionmaker(bind=engine)
        self.session = self.Session()

    def tearDown(self):
        self.session.close()

    def test_instance_creation(self):
        user = User(username="testuser", email="testuser@example.com", password="password")
        self.assertIsInstance(user, User)
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.email, "testuser@example.com")
        self.assertEqual(user.password, "password")

class TestImageModel(unittest.TestCase):
    def setUp(self):
        engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(engine)
        self.Session = sessionmaker(bind=engine)
        self.session = self.Session()

    def tearDown(self):
        self.session.close()

    def test_instance_creation(self):
        image = Image(user_id="some_user_id", file_path="/path/to/file", original_file_name="test.jpg")
        self.assertIsInstance(image, Image)
        self.assertEqual(image.user_id, "some_user_id")
        self.assertEqual(image.file_path, "/path/to/file")
        self.assertEqual(image.original_file_name, "test.jpg")

if __name__ == "__main__":
    unittest.main()
