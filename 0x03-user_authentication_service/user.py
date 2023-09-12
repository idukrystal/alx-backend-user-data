#!/usr/bin/env python3
""" Sqlalchemy relational mapping module for user """


from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class User(Base):
    """ Represents a single row in users table of database """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String)
    hashed_password = Column(String)
    session_id = Column(String)
    reset_token = Column(String)

    
