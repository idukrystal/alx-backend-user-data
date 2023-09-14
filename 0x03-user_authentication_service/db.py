#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """ Adds a new row to users table """
        user = User(email, hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **values) -> User:
        """ Finds a row in table corespinding to argument """
        result = self._session.query(User)
        for key, value in values.items():
            if key not in User.__dict__:
                raise InvalidRequestError
            for user in result:
                if getattr(user, key) == value:
                    return user
        raise NoResultFound

    def update_user(self, user_id: int, **values) -> None:
        """   updstes a users ddtails in d.b """
        try:
            user = self.find_user_by(id=user_id)
            print(user.hashed_password)
        except NoResultFound:
            raise valueError()
        for key, value in values.items():
            if hasattr(user, key):
                setattr(user, key, value)
            else:
                raise valueError()
        self._session.commit()
        u = self.find_user_by(id=user_id)
        print(u.hashed_password)
