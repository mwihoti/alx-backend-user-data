#!/usr/bin/env python3
"""
Auth module
"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """
    Hash Password
    """
    hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hash