#!/usr/bin/python3
# -*- coding: utf-8 -*-

from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, JSON, DateTime
from .base import Base


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)

    # 0: ADSL, 1: 4G LTE, 2: Phone
    atype: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    username: Mapped[str] = mapped_column(String(32), nullable=False)

    # just for '0' atype
    password: Mapped[str] = mapped_column(String(32), nullable=True)

    dname: Mapped[str] = mapped_column(String(32), nullable=True)

    data: Mapped[dict[str, str]] = mapped_column(JSON, nullable=True)

    # just for '0' atype
    cookies: Mapped[dict[str, str]] = mapped_column(JSON, nullable=True)

    created: Mapped[float] = mapped_column(DateTime, nullable=False, default=datetime.now())

    def __repr__(self):
        return f"<User(\
            id={self.id}, \
            username={self.username}, \
            password={self.password}, \
            dname={self.dname}, \
            data={self.data}, \
            cookies={self.cookies}, \
            created={self.created}\
            )>"
