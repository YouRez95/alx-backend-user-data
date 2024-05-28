#!/usr/bin/env python3
"""
    auth module
"""

import bcrypt


def _hash_password(plain_text_pass: str) -> str:
    '''
        hash the password
    '''
    bytes = plain_text_pass.encode('utf-8')
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(bytes, salt)
    return hash
