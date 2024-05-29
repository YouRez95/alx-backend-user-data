#!/usr/bin/env python3
"""
    auth module
"""

from typing import Union
import uuid
import bcrypt

from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    '''
        hash the password
    '''
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def _generate_uuid() -> str:
    '''
        generate unique id
    '''
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """
    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        '''
            register new user in to DB
        '''
        try:
            user = self._db.find_user_by(email=email)
            err_msg = 'User {} already exists'.format(email)
            raise ValueError(err_msg)
        except NoResultFound:
            hashed_password = _hash_password(password)
            return self._db.add_user(email, hashed_password)

    def valid_login(self, email: str, password: str) -> bool:
        '''
            login validation
        '''
        try:
            user = self._db.find_user_by(email=email)
            is_correct = bcrypt.checkpw(password.encode(),
                                        user.hashed_password)
            if is_correct:
                return True
            return False
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        '''
            create session and saved to database
        '''
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            # user.session_id = session_id
            # self._db._session.commit()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        '''
            search the user by session id
        '''
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        '''
            destroy session
        '''
        try:
            self._db.find_user_by(id=user_id)
            self._db.update_user(user_id, session_id=None)
        except NoResultFound:
            return None

    def get_reset_password_token(self, email: str) -> str:
        '''
            set the reset token and return it
        '''
        try:
            user = self._db.find_user_by(email=email)
            reset_token = _generate_uuid()
            self._db.update_user(user.id, reset_token=reset_token)
            return reset_token
        except NoResultFound:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        '''
            update password
        '''
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            hashed_password = _hash_password(password)
            self._db.update_user(user.id, hashed_password=hashed_password,
                                 reset_token=None)
        except NoResultFound:
            raise ValueError
