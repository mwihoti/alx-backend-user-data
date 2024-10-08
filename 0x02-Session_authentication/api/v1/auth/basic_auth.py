#!/usr/bin/env python3
"""
Module BasicAuth
"""
import base64
from typing import TypeVar
from models.user import User
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
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
        if type(user_email) == str and type(user_pwd) == str:
            try:
                users = User.search({'email': user_email})
            except Exception:
                return None
            if len(users) <= 0:
                return None
            if users[0].is_valid_password(user_pwd):
                return users[0]
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Basic overload current user
        Retrieve current user
        """
        auth_header = self.authorization_header(request)
        if auth_header is None:
            return None
        # Extract the Base64 part of the Authorization header
        base64_auth_header = self.extract_base64_authorization_header(
                auth_header)
        if base64_auth_header is None:
            return None

        # Decode the Base64 string to get the email:password
        decoded_auth_header = self.decode_base64_authorization_header(
                base64_auth_header)
        if decoded_auth_header is None:
            return None

        # Extract the email and password from the decoded string
        user_email, user_pwd = self.extract_user_credentials(
                decoded_auth_header)
        if user_email is None or user_pwd is None:
            return None

        # Retrieve the User instance based on the email and password
        user = self.user_object_from_credentials(user_email, user_pwd)
        return user
