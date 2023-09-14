#!/usr/bin/env python3
""" Module for user authentification """

import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """  converts password to byte  """
    return(bcrypt.hashpw(bytes(password, "ascii"), bcrypt.gensalt(rounds=15)))


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """ initialize new object """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ register new user """
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))
