#!/usr/bin/python3
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .base_model import BaseModel
from datetime import datetime

class Image(BaseModel):
    __tablename__ = 'images'
    
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    file_path = Column(String(256), nullable=False)
    original_file_name = Column(String(256), nullable=False)
    compressed_file_name = Column(String(256), nullable=True)
    upload_date = Column(DateTime, default=datetime.now)
    
    # Relationship to the User model
    user = relationship("User", back_populates="images")
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'upload_date' in kwargs:
            if isinstance(kwargs['upload_date'], str):
                try:
                    self.upload_date = datetime.fromisoformat(kwargs['upload_date'])
                except ValueError:
                    # Handle invalid date string format
                    self.upload_date = None
            elif isinstance(kwargs['upload_date'], datetime):
                self.upload_date = kwargs['upload_date']
            else:
                # Handle unexpected type
                self.upload_date = None

    def to_dict(self):
        dict_representation = super().to_dict()  # Use the base model's to_dict
        dict_representation["upload_date"] = self.upload_date.isoformat() if self.upload_date else None
        return dict_representation
