#!/usr/bin/env python3
"""
    auth module
"""

import bcrypt

from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    '''
        hash the password
    '''
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


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
