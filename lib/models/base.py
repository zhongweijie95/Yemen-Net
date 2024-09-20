#!/usr/bin/python3
# -*- coding: utf-8 -*-

from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy import create_engine


class Base(DeclarativeBase):
    ...


class DBEngine:
    DB_PATH: str = ""

    @classmethod
    def init_engine(cls):
        cls.Engine = create_engine(f"sqlite:///{cls.DB_PATH}", echo=False)
        return cls.Engine

    @classmethod
    def init_session(cls):
        cls.Session = sessionmaker(cls.Engine)
        return cls.Session

    @classmethod
    def init_db(cls):
        cls.init_engine()
        cls.init_session()
        Base.metadata.create_all(cls.Engine)