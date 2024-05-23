#!/usr/bin/env python3

'''
    class:
        Auth
'''


import uuid
from api.v1.auth.auth import Auth


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
