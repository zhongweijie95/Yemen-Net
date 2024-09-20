#!/usr/bin/python3
# -*- coding: utf-8 -*-

from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy import create_engine


class Base(DeclarativeBase):
    ...


class Engine:
    DB_PATH: str = ""

    @classmethod
    def engine(cls):
        return create_engine(f"sqlite:///{cls.DB_PATH}")

    @classmethod
    def session(cls):
        return sessionmaker(cls.engine())()

    @classmethod
    def init_db(cls):
        Base.metadata.create_all(cls.engine())

# Session.close_all()