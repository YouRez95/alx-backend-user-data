#!/usr/bin/env python3
"""
    auth module
"""

import bcrypt


def _hash_password(password: str) -> bytes:
    '''
        hash the password
    '''
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())
