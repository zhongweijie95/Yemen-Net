#!/usr/bin/python3
# -*- coding: utf-8 -*-

import typing
import flet as ft


class ClientStorage:
    def __init__(self, page: ft.Page):
        self._page = page
        self._client_storage = self._page.client_storage

    def add_user(self, atype: int | str, username: str, data: dict = {}) -> bool:
        if self._client_storage.contains_key(f"users.{atype}.{username}"):
            raise KeyError(f"{atype}.{username} is exists!")
        return self._client_storage.set(f"users.{atype}.{username}", data)

    def update_user_data(self, atype: int | str, username: str, data: dict) -> bool:
        return self._client_storage.set(f"users.{atype}.{username}", data)

    def update_user_data_key(self, atype: int | str, username: str, key: str, value: typing.Any):
        data = self.get_user_data(atype, username)
        data.update({key: value})
        self.update_user_data(atype, username, data)

    def get_user_data(self, atype: int | str, username: str) -> dict[str, typing.Any] | None:
        return self._client_storage.get(f"users.{atype}.{username}")

    def get_user_data_key(self, atype: int | str, username: str, key: str) -> typing.Any | None:
        return self._client_storage.get(f"users.{atype}.{username}").get(key)

    def remove_user(self, atype: int | str, username: str) -> bool:
        return self._client_storage.remove(f"users.{atype}.{username}")

    def is_exists(self, atype: int | str, username: str) -> bool:
        return self._client_storage.contains_key(f"users.{atype}.{username}")

    def get_users(self) -> list[tuple[str, str]]:
        return [
            u.removeprefix("users.").split(".")
            for u in self._client_storage.get_keys("users")
        ]
