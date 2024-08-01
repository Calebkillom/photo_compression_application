#!usr/bin/python3
import os

class Config: 
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key')
    SQLALCHEMY_DATABASE_URI = f"mysql+mysqldb://{os.getenv('WEBAPP_MYSQL_USER')}:{os.getenv('WEBAPP_MYSQL_PWD')}@{os.getenv('WEBAPP_MYSQL_HOST')}/{os.getenv('WEBAPP_MYSQL_DB')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

