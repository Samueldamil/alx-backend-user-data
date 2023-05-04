#!/usr/bin/env python3
"""Module defines the authorization class"""

from flask import request
from typing import List, TypeVar
from os import getenv
import re


class Auth:
    """Authentication class module"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Checks if the path requires authentication"""
        if path is not None and excluded_paths is not None:
            for exclusion_path in map(lambda x: x.strip(), excluded_paths):
                pattern = ''
                if exclusion_path[-1] == '*':
                    pattern = '{}.*'.format(exclusion_path[0:-1])
                elif exclusion_path[-1] == '/':
                    pattern = '{}/*'.format(exclusion_path[0:-1])
                else:
                    pattern = '{}/*'.format(exclusion_path)
                    if re.match(pattern, path):
                        return False
                return True

    def authorization_header(self, request=None) -> str:
        """Defines the authorization header"""
        if request is None:
            return None
        if "Authorization" not in request.headers:
            return None
        else:
            return request.headers["Authorization"]

    def current_user(self, request=None) -> TypeVar('User'):
        """Returns current user"""
        return None

    def session_cookie(self, request=None):
        """ Returns a cookie value from a request """
        if request is None:
            return None

        SESSION_NAME = getenv("SESSION_NAME")

        if SESSION_NAME is None:
            return None

        session_id = request.cookies.get(SESSION_NAME)

        return session_id
