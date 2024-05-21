#!/usr/bin/env python3

'''
    class:
        basic auth
'''


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
