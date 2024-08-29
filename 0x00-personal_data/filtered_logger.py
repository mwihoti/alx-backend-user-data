#!/usr/bin/env python3

"""
Function filter_datum that returns the log message obfuscted
"""
import logging
from typing import List
import re
import os
import mysql.connector


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """
    def filter_datum  Obfuscates specified fields in a log message.
    """
    # Create a regex pattern to match each field
    pattern = r';\s*(?P<field>{})=[^{}]*'.format('|'.join(fields), separator)

    def replace(match: re.Match) -> str:
        """
        Define the replacement function for the regex sub
        """
        field = match.group('field')
        return f"{separator}{field}={redaction}"
    # Perform the substitution using the regex pattern and replacement function
    return re.sub(pattern, replace, message)


def get_logger() -> logging.Logger:
    """returns a logging.Logger object.
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    get_db function that returns a connector to the database
    (mysql.connector.connection.MySQLConnection object).
    creates a connection to the database.
    """
    db_host = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    db_name = os.getenv('PERSONAL_DATA_DB_NAME', '')
    db_user = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    db_pwd = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
    connection = mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_pwd,
        database=db_name,
    )
    return connection


def main():
    """reads and retrieves all rows in the users table.
    """
    fields = "name,email,phone,ssn,password,ip,last_login,user_agent"
    columns = fields.split(',')
    query = "SELECT {} FROM users;".format(fields)
    info_logger = get_logger()
    connection = get_db()
    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()
        for row in rows:
            record = map(
                lambda x: '{}={}'.format(x[0], x[1]),
                zip(columns, row),
            )
            msg = '{};'.format('; '.join(list(record)))
            args = ("user_data", logging.INFO, None, None, msg, None, None)
            log_record = logging.LogRecord(*args)
            info_logger.handle(log_record)


class RedactingFormatter(logging.Formatter):
    """
    Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    FORMAT_FIELDS = ('name', 'levelname', 'asctime', 'message')
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """formats a LogRecord.
        """
        msg = super(RedactingFormatter, self).format(record)
        return filter_datum(self.fields, self.REDACTION, msg, self.SEPARATOR)


if __name__ == "__main__":
    main()
