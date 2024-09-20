#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import flet as ft
from lib.index import Application
from lib.models.base import DBEngine


def base_dir(*files):
    return os.path.join(os.path.dirname(__file__), *files)


if __name__ == "__main__":
    DBEngine.DB_PATH = base_dir("assets", "data.db")
    DBEngine.init_db()
    ft.app(target=Application())