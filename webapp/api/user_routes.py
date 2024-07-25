#!/usr/bin/python3

from flask import Blueprint, request, jsonify
from webapp.services.user_service import UserService
from webapp.utils.auth_utils import generate_token, decode_token

user_routes = Blueprint('user_routes', __name__)
user_service = UserService()

@user_routes.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()

    if not data:
        return jsonify({'message': 'No data provided'}), 400

    try:
        # Extract necessary fields from the request data
        username = data['username']
        password = data['password']
        email = data['email']
        firstname = data['firstname']
        lastname = data['lastname']
        
        # Register the user using the UserService
        user = user_service.register_user(username, password, email, firstname, lastname)
        
        # Check if user registration was successful
        if user:
            return jsonify({'message': 'User created successfully', 'user': user}), 201
        return jsonify({'message': 'User creation failed'}), 400
    except KeyError as e:
        return jsonify({'message': f'Missing required field: {str(e)}'}), 400

@user_routes.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    print("Received data:", data)  # Debugging line
    if 'username' not in data or 'password' not in data:
        return jsonify({'message': 'Missing required fields'}), 400
    user = user_service.authenticate_user(data['username'], data['password'])
    if user:
        token = generate_token(user['id'])
        return jsonify({'token': token}), 200
    return jsonify({'message': 'Invalid credentials'}), 401

@user_routes.route('/profile', methods=['GET'])
def profile():
    token = request.headers.get('Authorization').split()[1]
    user_id = decode_token(token)
    if user_id:
        user = user_service.get_user_by_id(user_id)
        if user:
            return jsonify(user.to_dict()), 200
    return jsonify({'message': 'Invalid or expired token'}), 401

@user_routes.route('/delete_account', methods=['DELETE'])
def delete_account():
    token = request.headers.get('Authorization').split()[1]
    user_id = decode_token(token)
    if user_id:
        success = user_service.delete_user(user_id)
        if success:
            return jsonify({'message': 'Account deleted successfully'}), 200
    return jsonify({'message': 'Invalid or expired token'}), 401

@user_routes.route('/logout', methods=['POST'])
def logout():
    # Since token-based authentication is stateless, there's no server-side session to invalidate.
    # Here, you would typically handle any cleanup if necessary, but for token-based auth, it's minimal.
    return jsonify({'message': 'Logout successful'}), 200
