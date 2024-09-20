#!/usr/bin/python3
# -*- coding: utf-8 -*-

import flet as ft
from .user_base import UserViewBase


class UserViewNew(UserViewBase):
    def __init__(self, page: ft.Page):
        super().__init__(page, ft.icons.PERSON_ADD_ALT_ROUNDED)

    def on_submit(self, e: ft.ControlEvent = None):
        super().on_submit(e)

        atype = int(self.drop_down.current.value)
        self.vm.add_user(
            atype,
            self.username.value, 
            self.password.value or (None if atype != 0 else "123456"),
            self.dname.value,
            None,
            None
        )

        self.on_submit_done()