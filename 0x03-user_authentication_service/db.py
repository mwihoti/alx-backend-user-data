#!/usr/bin/env python3
"""
DB module sqlalchemy
"""
from sqlalchemy import create_engine, tuple_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from user import User
from sqlalchemy.exc import InvalidRequestError
from user import Base


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
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
        """
        Add user to DB
        """
        NewUser = User(email=email, hashed_password=hashed_password)
        try:
            self._session.add(NewUser)
            self._session.commit()
        except Exception:
            self._session.rollback()
            NewUser = None
        return NewUser

    def find_user_by(self, **kwargs) -> User:
        """
        Find user by any field
        """
        session = self._session
        try:
            user = session.query(User).filter_by(**kwargs).one()
        except NoResultFound:
            raise NoResultFound()
        except InvalidRequestError:
            raise InvalidRequestError()
        return user

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        Update user
        """
        session = self._session
        user = self.find_user_by(id=user_id)
        for key, value in kwargs.items():
            setattr(user, key, value)
        try:
            session.commit()
        except InvalidRequestError:
            raise ValueError()
