#!/usr/bin/env python3
"""
Module of Auth views
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """
    Auth class
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Checks if a path requires authentication
        """
        return None

    def authorization_header(self, request=None) -> str:
        """
        Checks if the Authorization header is present
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Gets the current user
        """
        return None
