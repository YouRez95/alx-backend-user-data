#!/usr/bin/env python3

'''
    class:
        Auth
'''


from datetime import datetime
import os
from api.v1.auth.session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    '''
        sesionAuth handle the auth expiration date
    '''
    def __init__(self):
        '''
            initiate the duration
        '''
        try:
            self.session_duration = int(os.getenv('SESSION_DURATION', 0))
        except ValueError:
            self.session_duration = 0

    def create_session(self, user_id=None):
        '''
            create session with the date
        '''
        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        super().user_id_by_session_id[session_id] = {
            'user_id': user_id,
            'created_at': datetime.now()
        }
        return session_id

    def user_id_for_session_id(self, session_id=None):
        '''
            checking the duration before respond to the user
        '''
        if session_id is None or type(session_id) is not str:
            return None

        session_value = super().user_id_by_session_id.get(session_id)
        if session_value is None:
            return None

        if session_value.get('created_at') is None:
            return None
        rest_time = datetime.now() - session_value.get('created_at')
        session_duration = datetime.fromtimestamp(
            self.session_duration
            ).strftime("%H:%M:%S")
        if (int(str(rest_time).split(':')[1]) <
                int(session_duration.split(':')[1])):
            return session_value.get('user_id')
