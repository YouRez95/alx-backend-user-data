#!/usr/bin/env python3
"""
    auth module
"""

import bcrypt


def _hash_password(plain_text_pass: str) -> str:
    '''
        hash the password
    '''
    return bcrypt.hashpw(plain_text_pass.encode(), bcrypt.gensalt())
