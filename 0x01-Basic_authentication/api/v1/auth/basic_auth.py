#!/usr/bin/env python3

'''
    class:
        basic auth
'''

import base64
import binascii
from api.v1.auth.auth import Auth


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
