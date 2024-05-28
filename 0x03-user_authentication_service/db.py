#!/usr/bin/env python3
"""
    DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
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
        '''
            add new user to database
        '''
        if email is None or hashed_password is None:
            return None
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()
        return new_user

    def find_user_by(self, **kwargs):
        '''
            find user by argument and return it
        '''

        if not kwargs:
            raise InvalidRequestError
        column_names = User.__table__.columns.keys()
        for key in kwargs:
            if key not in column_names:
                raise InvalidRequestError

        result = self._session.query(User).filter_by(**kwargs).first()

        if result is None:
            raise NoResultFound
        return result