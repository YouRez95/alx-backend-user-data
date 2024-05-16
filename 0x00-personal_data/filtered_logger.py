#!/usr/bin/env python3

'''
    Regex-ing
'''

from typing import List
import re


import logging

PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def filter_datum(fields: List[str],
                 redaction: str, message: str, separator: str) -> str:
    '''
        function use a regex to replace
        occurrences of certain field value
    '''
    regex = '|'.join('(?<={}=).*?(?=\\{})'.format(field, separator)
                     for field in fields)
    return re.sub(regex, redaction, message)


def get_logger() -> logging.Logger:
    '''
        get_logger return a logger
    '''
    logger = logging.getLogger('user_data')
    stream = logging.StreamHandler()
    stream.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.setLevel(logging.INFO)
    logger.propagate = False
    logger.addHandler(stream)
    return logger


def get_db():
    pass


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        '''
            initialize
        '''
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        '''
            return the format desired
        '''
        msg = super(RedactingFormatter, self).format(record)
        text = filter_datum(self.fields, self.REDACTION, msg, self.SEPARATOR)
        return text
