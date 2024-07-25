#!/usr/bin/python3
from sqlalchemy import Column, String, DateTime
from .base_model import BaseModel

class User(BaseModel):
    __tablename__ = 'users'
    
    email = Column(String(128), nullable=False, unique=True)
    username = Column(String(128), nullable=False, unique=True)
    password = Column(String(128), nullable=False)
    first_name = Column(String(128), nullable=True)
    last_name = Column(String(128), nullable=True)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)