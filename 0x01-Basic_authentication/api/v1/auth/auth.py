#!/usr/bin/env python3

'''
    class:
        Auth
'''

from typing import List, TypeVar


class Auth:
    '''
        class manage the API authentication
    '''
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        '''
            require auth
        '''
        if path is None:
            return True
        if excluded_paths is None or not excluded_paths:
            return True
        if path[-1:] != '/':
            second_path = path + '/'
            if second_path in excluded_paths:
                return False
        if path in excluded_paths:
            return False

        return True

    def authorization_header(self, request=None) -> str:
        '''
            authorization header
        '''
        if request is None:
            return None
        value = request.headers.get('Authorization')
        return value

    def current_user(self, request=None) -> TypeVar('User'):  # type: ignore
        '''
            current user
        '''
        return None
