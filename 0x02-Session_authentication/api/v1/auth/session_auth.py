#!/usr/bin/env python3
"""
Module SessionAuth
"""
import base64
from typing import TypeVar
from models.user import User
from api.v1.auth.auth import Auth
import uuid


class SessionAuth(Auth):
    """
    class SessionAuth
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        creates a session Id
        """
        if user_id is None or not isinstance(user_id, str):
            return None

        sessionID = str(uuid.uuid4())
        self.user_id_by_session_id[sessionID] = user_id
        return sessionID

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        returns a User ID based on a Session ID
        """
        if session_id is None or not isinstance(session_id, str):
            return None

        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """
        Returns a User instance based on a session cookie
        """
        sessionID = self.session_cookie(request)
        if sessionID is None:
            return None

        user_id = self.user_id_for_session_id(sessionID)
        if user_id is None:
            return None

        return User.get(user_id)

    def destroy_session(self, request=None):
        """
        Deletes users session
        """
        if request is None:
            return False

        sessionID = self.session_cookie(request)
        if sessionID is None:
            return False

        user_id = self.user_id_by_session_id(sessionID)
        if user_id is None:
            return False

        del self.user_id_by_session_id[sessionID]
        return True