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
        Returns True if path is None
        Returns True if excluded_paths is None or empty
        Returns False if path is in excluded_paths
        You can assume excluded_paths contains string path always ending by a /
        """
        if path is None:
            return True
        if excluded_paths is None or not excluded_paths:
            return True
        # Ensure the path ends with a slash for comparison
        if not path.endswith('/'):
            path += '/'

        # Check if the normalized path is in the list of excluded_paths
        for excluded_path in excluded_paths:
            if excluded_path.endswith('/') and path == excluded_path:
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """
        Checks if the Authorization header is present
        If request is None, returns None
        If request doesn’t contain the header key Authorization, returns None
        Otherwise, return the value of the header request Authorization
        """
        if request is None:
            return None
        auth_header = request.headers.get('Authorization')
        if auth_header is None:
            return None
        return auth_header

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Gets the current user
        """
        return None
