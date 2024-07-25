#!/usr/bin/python3

from webapp.models import User
from webapp.engine import get_session

class UserRepository:
    @staticmethod
    def create_user(session, user_data):
        user = User(**user_data)
        session.add(user)
        session.commit()
        return user

    @staticmethod
    def find_user_by_id(session, user_id):
        return session.query(User).filter_by(id=user_id).first()

    @staticmethod
    def find_user_by_username(session, username):
        return session.query(User).filter_by(username=username).first()

    @staticmethod
    def update_user(session, user_id, user_data):
        user = UserRepository.find_user_by_id(session, user_id)
        if user:
            for key, value in user_data.items():
                setattr(user, key, value)
            session.commit()
        return user

    @staticmethod
    def delete_user(session, user_id):
        user = UserRepository.find_user_by_id(session, user_id)
        if user:
            session.delete(user)
            session.commit()
            return True
        return False
