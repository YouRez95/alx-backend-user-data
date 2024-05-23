#!/usr/bin/env python3

'''
    class:
        Auth
'''


import uuid
from api.v1.auth.auth import Auth
from models.user import User


class SessionAuth(Auth):
    '''
        class session Auth
    '''
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        '''
            method that can create session
        '''
        if user_id is None or type(user_id) is not str:
            return None

        session_id = str(uuid.uuid4())
        SessionAuth.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        '''
            method that can retrieve the user_id by session_id
        '''
        if session_id is None or type(session_id) is not str:
            return None
        user_id = SessionAuth.user_id_by_session_id.get(session_id)
        return None if user_id is None else user_id

    def current_user(self, request=None):
        '''
            get the current user based on the session id
        '''
        session_id = self.session_cookie(request)
        if session_id is None:
            return None
        user_id = self.user_id_for_session_id(session_id)
        return User.get(user_id)

    def destroy_session(self, request=None):
        '''
            destroy session
        '''
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if session_id is None:
            return False

        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return False

        del self.user_id_by_session_id[session_id]
        return True
