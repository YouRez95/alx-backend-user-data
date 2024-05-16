#!/usr/bin/env python3

'''
    Regex-ing
'''

from typing import List
import re


import logging


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        '''
            return the format desired
        '''
        msg = super(RedactingFormatter, self).format(record)
        text = filter_datum(self.fields, self.REDACTION, msg, self.SEPARATOR)
        return text


def filter_datum(fields: List[str],
                 redaction: str, message: str, separator: str) -> str:
    '''
        function use a regex to replace
        occurrences of certain field value
    '''
    regex = '|'.join('(?<={}=).*?(?=\\{})'.format(field, separator)
                     for field in fields)
    return re.sub(regex, redaction, message)
