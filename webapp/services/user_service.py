#!/usr/bin/python3
import logging
from webapp.repositories.user_repository import UserRepository
from webapp.engine.storage_engine import get_session  # Import get_session function
from webapp.utils.auth_utils import check_password, hash_password

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class UserService:
    @staticmethod
    def register_user(username, password, email, firstname, lastname):
        session = get_session()
        try:
            # Input validation
            if not username or not password or not email:
                raise ValueError("Username, password, and email are required")
            
            hashed_password = hash_password(password)
            
            # Check if user already exists
            if UserRepository.find_user_by_username(session, username):
                raise ValueError("Username already exists")
            
            user = UserRepository.create_user(session, {
                'username': username,
                'password': hashed_password,
                'email': email,
                'first_name': firstname,
                'last_name': lastname
            })
            
            # Commit the transaction
            session.commit()  # Use session.commit() instead of storage.save()
            
            logging.info(f"User registered: {username}")
            return user.to_dict()
        
        except ValueError as e:
            logging.error(f"Value error: {e}")
            return None
        
        except Exception as e:
            logging.error(f"Error registering user: {e}")
            return None
        
        finally:
            session.close()

    @staticmethod
    def authenticate_user(username, password):
        session = get_session()
        try:
            user = UserRepository.find_user_by_username(session, username)
            if user and check_password(user.password, password):
                logging.info(f"User authenticated: {username}")
                return user.to_dict()
            logging.warning(f"Authentication failed for user: {username}")
            return None
        
        except Exception as e:
            logging.error(f"Error authenticating user: {e}")
            return None
        
        finally:
            session.close()

    @staticmethod
    def update_user_profile(user_id, firstname, lastname):
        session = get_session()
        try:
            user = UserRepository.find_user_by_id(session, user_id)
            if user:
                user.first_name = firstname
                user.last_name = lastname
                UserRepository.save_user(session, user)  # Assuming save_user is a method in UserRepository
                logging.info(f"User profile updated: {user_id}")
                return user.to_dict()
            
            logging.warning(f"User not found for update: {user_id}")
            return None
        
        except Exception as e:
            logging.error(f"Error updating user profile: {e}")
            return None
        
        finally:
            session.close()

    @staticmethod
    def delete_user(user_id):
        session = get_session()
        try:
            user = UserRepository.find_user_by_id(session, user_id)
            if user:
                UserRepository.delete_user(session, user)  # Assuming delete_user is a method in UserRepository
                logging.info(f"User deleted: {user_id}")
                return True
            
            logging.warning(f"User not found for deletion: {user_id}")
            return False
        
        except Exception as e:
            logging.error(f"Error deleting user: {e}")
            return False
        
        finally:
            session.close()
