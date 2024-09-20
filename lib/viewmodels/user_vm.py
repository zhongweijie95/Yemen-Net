#!/usr/bin/python3
# -*- coding: utf-8 -*-

from ..models.base import DBEngine
from ..models.user import User


class UserViewModel:
    def __init__(self):
        self.session = DBEngine.Session()

    @property
    def users(self) -> list[User]:
        return self.session.query(User).all()

    def get_users(self) -> list[User]:
        return self.session.query(User).all()

    def add_user(self, 
                 atype: int,
                 username: str,
                 password: str,
                 dname: str,
                 data: dict[str, str] = None,
                 cookies: dict[str, str] = None) -> None:

        new_user = User(
            atype=atype,
            username=username,
            password=password,
            dname=dname,
            data=data,
            cookies=cookies
        )
        self.session.add(new_user)
        self.session.commit()

    def delete_user(self, user_id: int) -> None:
        if (user := self.session.query(User).filter_by(id=user_id).first()):
            self.session.delete(user)
            self.session.commit()

    def edit_data_and_cookies(self, 
                              user_id: int,
                              data: dict[str, str], 
                              cookies: dict[str, str]):

        if (user := self.session.query(User).filter_by(id=user_id).first()):
            user.data = data
            user.cookies = cookies
            self.session.commit()

    def edit_user(self, 
                  user_id: int, 
                  atype: int,
                  username: str,
                  password: str,
                  dname: str) -> None:

        if (user := self.session.query(User).filter_by(id=user_id).first()):
            if user.atype != atype:
                # change account type
                user.atype = atype
                if atype != 0:
                    user.password = None
                    user.data = None
                else:
                    user.username = username
                    user.password = password or "123456"
            else:
                # change username or password
                user.username = username
                user.password = password

            user.dname = dname
            user.cookies = None

            self.session.commit()

    def get_user(self, user_id: int) -> User:
        return self.session.query(User).filter_by(id=user_id).first()

    def __del__(self):
        self.session.close()