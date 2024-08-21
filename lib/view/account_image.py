#!/usr/bin/python3
# -*- coding: utf-8 -*-

import flet as ft


class YAccountImage(ft.CircleAvatar):
    _images = ('adsl', 'lte', 'phone')

    def __init__(self, name: str | int = None):
        super().__init__()

        self.content = ft.Image(
            filter_quality = ft.FilterQuality.HIGH,
            fit=ft.ImageFit.CONTAIN
        )

        self.set_image(name)

        self.color = ft.colors.TRANSPARENT
        self.bgcolor = ft.colors.TRANSPARENT

    def set_image(self, name: str | int) -> None:
        if isinstance(name, int):
            name = self._images[name]
        self.content.src = f"assets/{name}.png"
