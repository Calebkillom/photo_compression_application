#!/usr/bin/python3

from webapp.models import Image
from webapp.engine import get_session

class ImageRepository:
    @staticmethod
    def create_image(session, image_data):
        # Debug: Print the type and content of image_data
        print(f"DEBUG: image_data (type): {type(image_data)}")
        print(f"DEBUG: image_data (content): {image_data}")

        # Check if image_data is an instance of Image
        if isinstance(image_data, Image):
            # Directly use the Image instance
            image = image_data
        elif isinstance(image_data, dict):
            # Convert dictionary to Image instance
            required_fields = {'user_id', 'file_path', 'original_file_name'}
            if not required_fields.issubset(image_data.keys()):
                raise ValueError("Missing required fields in image_data")
            
            image = Image(
                user_id=image_data.get('user_id'),
                file_path=image_data.get('file_path'),
                original_file_name=image_data.get('original_file_name'),
                compressed_file_name=image_data.get('compressed_file_name'),
                upload_date=image_data.get('upload_date')
            )
        else:
            raise TypeError("image_data must be an Image instance or a dictionary")

        # Debug: Print the created Image object
        print(f"DEBUG: Created Image object: {image}")

        # Add to session and commit
        session.add(image)
        session.commit()
        print("DEBUG: Image committed to session")

        return image

    @staticmethod
    def get_image_by_id(session, image_id):
        return session.query(Image).filter_by(id=image_id).first()

    @staticmethod
    def get_images_by_user_id(session, user_id):
        return session.query(Image).filter_by(user_id=user_id).all()

    @staticmethod
    def update_image(session, image_id, image_data):
        image = ImageRepository.get_image_by_id(session, image_id)
        if image:
            for key, value in image_data.items():
                setattr(image, key, value)
            session.commit()
        return image

    @staticmethod
    def delete_image(session, image_id):
        image = ImageRepository.get_image_by_id(session, image_id)
        if image:
            session.delete(image)
            session.commit()
            return True
        return False

    @staticmethod
    def search_images(session, user_id, search_term):
        query = session.query(Image)
        if user_id:
            query = query.filter_by(user_id=user_id)
        if search_term:
            query = query.filter(Image.original_file_name.ilike(f"%{search_term}%"))
        return query.all()
