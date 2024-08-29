#!/usr/bin/env python3
"""
Encrypting passwords: Password should not be stored in plain text in a databse
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """
    hash_password function that expects a string password and returns a salted
    hashed password,which is a byte string.
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    is_valid function that expects 2 arguments and returns a boolean.
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
