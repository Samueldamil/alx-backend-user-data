#!/usr/bin/env python3
"""
Handling personal data
"""
import logging
from typing import List
import re
from os import environ
import mysql.connector

PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """ Return a Logger object """
    for f in fields:
        message = re.sub(f'{f}=.*?{separator}',
                         f'{f}={redaction}{separator}', message)
    return message


def get_logger() -> logging.Logger:
    """ Returns a Logger object """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    streamhdlr = logging.StreamHandler()
    streamhdlr.setFormatter(RedactingFormatter(list(PII_FIELDS)))
    logger.addHandler(streamhdlr)

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """ Return a connector to a MySQL Database """
    username = environ.get("PERSONAL_DATA_DB_USERNAME")
    password = environ.get("PERSONAL_DATA_DB_PASSWORD")
    host = environ.get("PERSONAL_DATA_DB_HOST")
    db_name = environ.get("PERSONAL_DATA_DB_NAME")

    connec = mysql.connector.connection.MySQLConnection(user=username,
                                                        password=password,
                                                        host=host,
                                                        database=db_name)
    return connec


def main():
    """ Read and filter data """
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    field_names = [i[0] for i in cursor.description]

    logger = get_logger()

    for row in cursor:
        str_row = ''.join(f'{f}={str(r)}; ' for r, f in zip(row, field_names))
        logger.info(str_row.strip())

    cursor.close()
    db.close()


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ Log formatter """
        record.msg = filter_datum(self.fields, self. REDACTION,
                                  record.getMessage(), self.SEPARATOR)
        return super(RedactingFormatter, self).format(record)
