#!/usr/bin/env python3

'''
    class:
        Auth
'''

from flask import request
from typing import List, TypeVar


class Auth:
    '''
        class manage the API authentication
    '''
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        '''
            require auth
        '''
        return False

    def authorization_header(self, request=None) -> str:
        '''
            authorization header
        '''
        return None

    def current_user(self, request=None) -> TypeVar('User'):  # type: ignore
        '''
            current user
        '''
        return None
