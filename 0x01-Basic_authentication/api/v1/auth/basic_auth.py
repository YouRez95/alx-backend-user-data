#!/usr/bin/env python3

'''
    class:
        basic auth
'''

import base64
import binascii
from api.v1.auth.auth import Auth
from typing import Tuple, TypeVar

from models.base import Base
from models.user import User


class BasicAuth(Auth):
    '''
        basic auth class
    '''
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        '''
            extract the base64 from the header
        '''
        if (authorization_header is None or
                not isinstance(authorization_header, str)):
            return None
        if authorization_header[:6] == 'Basic ':
            return authorization_header[6:]

        return None

    def decode_base64_authorization_header(
                                    self,
                                    base64_authorization_header: str) -> str:
        '''
            decode the base64 authorization header
        '''
        if (base64_authorization_header is None or
                not isinstance(base64_authorization_header, str)):
            return None

        try:
            decoded = base64.b64decode(
                base64_authorization_header).decode('utf-8')
            return decoded
        except binascii.Error:
            return None

    def extract_user_credentials(
                self,
                decoded_base64_authorization_header: str) -> Tuple[str, str]:
        '''
            returns the user email and password from the Base64 decoded value
        '''

        if (decoded_base64_authorization_header is None or
                not isinstance(decoded_base64_authorization_header, str)):
            return (None, None)

        if ':' in decoded_base64_authorization_header:
            user_pass = decoded_base64_authorization_header.split(':')
            return (user_pass[0], user_pass[1])
        return (None, None)

    def user_object_from_credentials(
            self, user_email: str,
            user_pwd: str) -> TypeVar('User'):  # type: ignore
        '''
            returns the User instance based on his email and password
        '''
        if (user_email is None or
                not isinstance(user_email, str) or
                user_pwd is None or not isinstance(user_pwd, str)):
            return None
        user = User.search({'email': user_email})
        if not user or not user[0]:
            return None
        is_valid = user[0].is_valid_password(user_pwd)
        if is_valid:
            return user[0]
        return None
