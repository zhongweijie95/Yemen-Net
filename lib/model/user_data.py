#!/usr/bin/python3
# -*- coding: utf-8 -*-

import humanize
from datetime import datetime


class UserData:
    def __init__(self, data: dict[str, str]):
        self._data = data

    @classmethod
    def calc_credit(self, value: float) -> str:
        return humanize.naturalsize(value * 10**9, format="%.2f")

    @property
    def credit(self) -> str:
        value = float(self._data.get("valid_credit").split()[0].strip())
        return humanize.naturalsize(value * 10**9, format="%.2f")

    @property
    def expir_date(self) -> str:
        return self._data.get("credit_expiry_date")

    @property
    def name(self) -> str:
        return self._data.get("name")
    
    @property
    def status(self) -> bool:
        return "active" in self._data.get("current_account_status")

    @property
    def atype(self) -> str:
        return self._data.get("account_type")
