#!/usr/bin/python3
# services/image_service.py

from webapp.models import Image
from webapp.repositories import ImageRepository
from webapp.engine import get_session
import zstandard as zstd
import requests

class ImageService:
    @staticmethod
    def upload_image(file_path, original_file_name, compressed_file_name, user_id):
        session = get_session()
        try:
            image = Image(file_path=file_path, original_file_name=original_file_name,
                          compressed_file_name=compressed_file_name, user_id=user_id)
            ImageRepository.create_image(session, image)
            return image.to_dict()
        finally:
            session.close()

    @staticmethod
    def compress_image(image_id, compression_level):
        session = get_session()
        try:
            image = ImageRepository.get_image_by_id(session, image_id)
            if image:
                compressor = zstd.ZstdCompressor(level=compression_level)
                with open(image.file_path, 'rb') as f_in:
                    compressed_data = compressor.compress(f_in.read())
                
                image.compressed_file_name = image.file_path + '.zst'
                
                with open(image.compressed_file_name, 'wb') as f_out:
                    f_out.write(compressed_data)
                
                image.save(session)
                return image.to_dict()
            return None
        finally:
            session.close()

    @staticmethod
    def decompress_image(image_id):
        session = get_session()
        try:
            image = ImageRepository.get_image_by_id(session, image_id)
            if image and image.compressed_file_name:
                decompressor = zstd.ZstdDecompressor()
                with open(image.compressed_file_name, 'rb') as f_in:
                    decompressed_data = decompressor.decompress(f_in.read())
                
                image.file_path = image.compressed_file_name.replace('.zst', '')
                
                with open(image.file_path, 'wb') as f_out:
                    f_out.write(decompressed_data)
                
                image.save(session)
                return image.to_dict()
            return None
        finally:
            session.close()

    @staticmethod
    def delete_image(image_id):
        session = get_session()
        try:
            image = ImageRepository.get_image_by_id(session, image_id)
            if image:
                image.delete(session)
                return True
            return False
        finally:
            session.close()

    @staticmethod
    def search_images(user_id, search_term):
        session = get_session()
        try:
            images = ImageRepository.search_images(session, user_id, search_term)
            return [image.to_dict() for image in images]
        finally:
            session.close()

    @staticmethod
    def upload_from_url(url, service, access_token, user_id):
        """
        Upload an image from a URL provided by Google Drive or Dropbox.
        """
        # Download the image from the URL
        headers = {'Authorization': f'Bearer {access_token}'} if access_token else {}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            file_content = response.content
            # Generate a unique filename or use a meaningful name
            original_file_name = url.split('/')[-1]
            file_path = f"uploads/{original_file_name}"
            compressed_file_name = f"{file_path}.zst"

            # Save the image to a file
            with open(file_path, 'wb') as f:
                f.write(file_content)
            
            # Compress the image
            image = ImageService.upload_image(file_path, original_file_name, compressed_file_name, user_id)
            ImageService.compress_image(image['id'], compression_level=3)  # Example compression level
            return image
        else:
            return None
