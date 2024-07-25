from flask import Blueprint, request, jsonify, send_from_directory
from webapp.services.image_service import ImageService
from webapp.utils.auth_utils import decode_token
import requests
import json
import os

image_routes = Blueprint('image_routes', __name__)
image_service = ImageService()

def get_user_id_from_token():
    token = request.headers.get('Authorization')
    if token:
        try:
            return decode_token(token.split()[1])  # Extract token part after 'Bearer'
        except Exception as e:
            return None
    return None

@image_routes.route('/upload', methods=['POST'])
def upload_image():
    user_id = get_user_id_from_token()
    if user_id:
        file = request.files.get('image')
        if file:
            file_path = f'/tmp/{file.filename}'
            file.save(file_path)
            compressed_file_name = file_path + '.zst'
            compressed_image = image_service.upload_image(file_path, file.filename, compressed_file_name, user_id)
            return jsonify({'message': 'Image uploaded and compressed', 'image': compressed_image}), 201
        return jsonify({'message': 'No image file provided'}), 400
    return jsonify({'message': 'Invalid or expired token'}), 401

@image_routes.route('/upload-from-google-drive', methods=['POST'])
def upload_from_google_drive():
    user_id = get_user_id_from_token()
    if user_id:
        google_drive_file_id = request.json.get('file_id')
        if not google_drive_file_id:
            return jsonify({'message': 'No Google Drive file ID provided'}), 400

        headers = {'Authorization': 'Bearer ' + request.json.get('access_token')}
        metadata_url = f'https://www.googleapis.com/drive/v3/files/{google_drive_file_id}?fields=name'
        metadata_response = requests.get(metadata_url, headers=headers)

        if metadata_response.status_code == 200:
            file_metadata = metadata_response.json()
            file_name = file_metadata.get('name')
            if not file_name:
                return jsonify({'message': 'Failed to get file name from metadata'}), 500

            download_url = f'https://www.googleapis.com/drive/v3/files/{google_drive_file_id}?alt=media'
            file_response = requests.get(download_url, headers=headers)
            if file_response.status_code == 200:
                file_content = file_response.content
                file_path = f'/tmp/{file_name}'
                with open(file_path, 'wb') as f:
                    f.write(file_content)

                compressed_file_name = file_path + '.zst'
                compressed_image = image_service.upload_image(file_path, file_name, compressed_file_name, user_id)
                return jsonify({'message': 'Image uploaded and compressed', 'image': compressed_image}), 201
            return jsonify({'message': 'Failed to download file from Google Drive'}), 500
        return jsonify({'message': 'Failed to fetch file metadata from Google Drive'}), 500
    return jsonify({'message': 'Invalid or expired token'}), 401

@image_routes.route('/upload-from-dropbox', methods=['POST'])
def upload_from_dropbox():
    user_id = get_user_id_from_token()
    if user_id:
        dropbox_file_path = request.json.get('file_path')
        if not dropbox_file_path:
            return jsonify({'message': 'No Dropbox file path provided'}), 400

        headers = {
            'Authorization': 'Bearer ' + request.json.get('access_token'),
            'Content-Type': 'application/json'
        }
        metadata_url = 'https://api.dropboxapi.com/2/files/get_metadata'
        metadata_payload = {"path": dropbox_file_path}
        metadata_response = requests.post(metadata_url, headers=headers, json=metadata_payload)

        if metadata_response.status_code == 200:
            file_metadata = metadata_response.json()
            file_name = file_metadata.get('name')
            if not file_name:
                return jsonify({'message': 'Failed to get file name from metadata'}), 500

            download_url = 'https://content.dropboxapi.com/2/files/download'
            download_headers = {
                'Authorization': 'Bearer ' + request.json.get('access_token'),
                'Dropbox-API-Arg': json.dumps({"path": dropbox_file_path})
            }
            file_response = requests.post(download_url, headers=download_headers)
            if file_response.status_code == 200:
                file_content = file_response.content
                file_path = f'/tmp/{file_name}'
                with open(file_path, 'wb') as f:
                    f.write(file_content)

                compressed_file_name = file_path + '.zst'
                compressed_image = image_service.upload_image(file_path, file_name, compressed_file_name, user_id)
                return jsonify({'message': 'Image uploaded and compressed', 'image': compressed_image}), 201
            return jsonify({'message': 'Failed to download file from Dropbox'}), 500
        return jsonify({'message': 'Failed to fetch file metadata from Dropbox'}), 500
    return jsonify({'message': 'Invalid or expired token'}), 401

@image_routes.route('/gallery', methods=['GET'])
def gallery():
    user_id = get_user_id_from_token()
    if user_id:
        images = image_service.get_images_by_user(user_id)
        return jsonify([image.to_dict() for image in images]), 200
    return jsonify({'message': 'Invalid or expired token'}), 401

@image_routes.route('/delete/<int:image_id>', methods=['DELETE'])
def delete_image(image_id):
    user_id = get_user_id_from_token()
    if user_id:
        success = image_service.delete_image(image_id)
        if success:
            return jsonify({'message': 'Image deleted successfully'}), 200
    return jsonify({'message': 'Invalid or expired token'}), 401

@image_routes.route('/download/<int:image_id>', methods=['GET'])
def download_image(image_id):
    user_id = get_user_id_from_token()
    if user_id:
        image = image_service.get_image_by_id(image_id)
        if image and image.compressed_file_name:
            file_path = image.compressed_file_name
            # Ensure the file exists
            if os.path.exists(file_path):
                return send_from_directory(directory='/tmp', filename=os.path.basename(file_path), as_attachment=True)
            return jsonify({'message': 'File not found'}), 404
        return jsonify({'message': 'Invalid image ID or file path'}), 404
    return jsonify({'message': 'Invalid or expired token'}), 401

@image_routes.route('/search', methods=['GET'])
def search_images():
    user_id = get_user_id_from_token()
    if user_id:
        query = request.args.get('query')
        images = image_service.search_images(user_id, query)
        return jsonify([image.to_dict() for image in images]), 200
    return jsonify({'message': 'Invalid or expired token'}), 401
