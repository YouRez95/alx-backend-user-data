#!/usr/bin/env python3

'''
    class:
        SessionAuth
'''
import uuid
from api.v1.auth.auth import Auth


class SessionAuth(Auth):
    '''
        class that handle the session auth
    '''
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        '''
            method that can create sessionId
        '''
        if user_id is None or type(user_id) is not str:
            return None
        session_id = str(uuid.uuid4())
        SessionAuth.user_id_by_session_id[session_id] = user_id
        return session_id
