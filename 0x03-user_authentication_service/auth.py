#!/usr/bin/env python3
""" Module for user authentification """

import bcrypt
from uuid import uuid4
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from typing import Union


def _hash_password(password: str) -> bytes:
    """  converts password to byte  """
    return (bcrypt.hashpw(bytes(password, "ascii"), bcrypt.gensalt(rounds=15)))


def _generate_uuid() -> str:
    """ generates unique uid's """
    return str(uuid4())


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

    def valid_login(self, email: str, password: str) -> bool:
        """ Check if a valid login is made """
        try:
            user = self._db.find_user_by(email=email)
            if bcrypt.checkpw(bytes(password, "ascii"), user.hashed_password):
                return True
            return False
        except NoResultFound:
            return False

    def create_session(self, email: str) -> Union[str, None]:
        """ regusters a users session id """
        try:
            user = self._db.find_user_by(email=email)
            uid = _generate_uuid()
            self._db.update_user(user.id, session_id=uid)
            return uid
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """ returns tge user who owns session_id """
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """ Deletes a user session uuid """
        try:
            self._db.update_user(user_id, session_id=None)
        except ValueError:
            return

    def get_reset_password_token(self, email: str) -> str:
        """ generates a password reset token """
        try:
            user = self._db.find_user_by(email=email)
            uid = _generate_uuid()
            self._db.update_user(user.id, reset_token=uid)
            return uid
        except NoResultFound:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """ resets a user's password """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            self._db.update_user(
                user.id,
                hashed_password=_hash_password(password),
                reset_token=None
            )
        except NoResultFound:
            raise ValueError
