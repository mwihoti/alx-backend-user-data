#!/usr/bin/env python3
"""
Module BasicAuth
"""
import base64
from typing import TypeVar
from models.user import User


class BasicAuth:
    """
    BasicAuth class
    """

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """
        Return None if authorization_header is None
        Return None if authorization_header is not a string
        Return None if authorization_header doesn’t start by Basic
        (with a space at the end)
        Otherwise, return the value after Basic (after the space)
        """
        if authorization_header is None or not isinstance(authorization_header,
                                                          str):
            return None

        if not authorization_header.startswith('Basic '):
            return None
        return authorization_header[len('Basic '):]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """ Return None if base64_authorization_header is None
        Return None if base64_authorization_header is not a string
        Return None if base64_authorization_header is not a valid Base64
        you can use try/except
        """
        if base64_authorization_header is None or not isinstance(
                base64_authorization_header, str):
            return None
        try:
            decode_byte = base64.b64decode(base64_authorization_header)
            return decode_byte.decode('utf-8')
        except (base64.binascii.Error, UnicodeDecodeError):
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """
        Basic - User credentials
        Return None if decoded_base64_authorization_header is None
        Return None, None if decoded_base64_authorization_header is None
        Return None, None if decoded_base64_authorization_header
        """
        if decoded_base64_authorization_header is None or not isinstance(
                decoded_base64_authorization_header, str):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None

        email, password = decoded_base64_authorization_header.split(':', 1)
        return email, password

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """
        Basic - User object
        Return None if user_email is None or not a string
        Return None if user_pwd is None or not a string
        """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        users = User.search({"email": user_email})
        if not users or len(users) == 0:
            return None

        user = users[0]
        if not user.is_valid_password(user_pwd):
            return None

        return user

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Basic overload current user
        Retrieve current user
        """
        auth_header = self.authorization_header(request)
        b64_auth_token = self.extract_base64_authorization_header(auth_header)
        auth_token = self.decode_base64_authorization_header(b64_auth_token)
        email, password = self.extract_user_credentials(auth_token)
        return self.user_object_from_credentials(email, password)
