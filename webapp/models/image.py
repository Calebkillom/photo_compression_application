#!/usr/bin/python3
from sqlalchemy import Column, String, DateTime, ForeignKey
from .base_model import BaseModel
from datetime import datetime

class Image(BaseModel):
    __tablename__ = 'images'
    
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    file_path = Column(String(256), nullable=False)
    original_file_name = Column(String(256), nullable=False)
    compressed_file_name = Column(String(256), nullable=True)
    upload_date = Column(DateTime, default=datetime.now)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)