#!/usr/bin/env python3

'''
    Regex-ing
'''

from typing import List
import re


def filter_datum(fields: List[str],
                 redaction: str, message: str, separator: str) -> str:
    '''
        function use a regex to replace
        occurrences of certain field value
    '''
    regex = '|'.join('(?<={}=).*?(?=\\{})'.format(field, separator)
                     for field in fields)
    return re.sub(regex, redaction, message)
