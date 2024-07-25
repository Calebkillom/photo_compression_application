#!/usr/bin/python3
# webapp/engine/storage_engine.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from os import getenv
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

Base = declarative_base()

class DBStorage:
    def __init__(self):
        user = getenv('WEBAPP_MYSQL_USER')
        password = getenv('WEBAPP_MYSQL_PWD')
        host = getenv('WEBAPP_MYSQL_HOST')
        db = getenv('WEBAPP_MYSQL_DB')

        # Log the environment variables (mask sensitive info)
        logging.info(f"User: {user}, Host: {host}, DB: {db}")

        # Check if any of the environment variables are None
        if not all([user, password, host, db]):
            raise ValueError("One or more environment variables are not set")

        self.__engine = create_engine(
            f"mysql+mysqldb://{user}:{password}@{host}/{db}",
            pool_pre_ping=True)
        if getenv('WEBAPP_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)
        
        self.__session = None  # Initialize session as None
        self.reload()  # Set up session

    def all(self, cls=None):
        from webapp.models import User, Image  # Import relevant models
        objects = {}
        classes = [User, Image]  # Add other models as needed
        if cls:
            classes = [cls]
        for cl in classes:
            for obj in self.__session.query(cl).all():
                key = f"{obj.__class__.__name__}.{obj.id}"
                objects[key] = obj
        return objects
    
    def new(self, obj):
        self.__session.add(obj)
    
    def save(self):
        self.__session.commit()
    
    def delete(self, obj=None):
        if obj:
            self.__session.delete(obj)
    
    def reload(self):
        from webapp.models.base_model import Base  # Ensure Base is from models.base_model
        from webapp.models.user import User  # Import User model
        from webapp.models.image import Image  # Import Image model

        Base.metadata.create_all(self.__engine)
        self.__session = scoped_session(sessionmaker(bind=self.__engine, expire_on_commit=False))

    @property
    def session(self):
        if self.__session is None:
            self.reload()  # Ensure session is loaded
        return self.__session

# Create an instance of DBStorage
storage = DBStorage()

# Define the get_session function
def get_session():
    return storage.session
