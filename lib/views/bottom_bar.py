#!/usr/bin/python3
# -*- coding: utf-8 -*-


import flet as ft
from .about import About
from ..constant import THEME_COLORS, ThemeController


class BottomAppBar(ft.BottomAppBar):
    def __init__(self, page: ft.Page):
        super().__init__()

        self.page = page
        self.page.on_resized = self.on_window_resize

        self.height = 75
        self.notch_margin = 8
        self.shape = ft.NotchShape.CIRCULAR
        self.padding = ft.padding.only(left=5, right=5, top=20)
        self.content = ft.Row(
            controls=[
                ft.IconButton(
                    icon=ft.icons.INFO,
                    on_click=self.open_about_dialog
                ),
                ft.RadioGroup(
                    value=self.page.theme.color_scheme_seed.upper(),
                    content=ft.ListView(
                        horizontal=True,
                        spacing=0,
                        width=self.page.window.width - 150,
                        controls=[
                            ft.Radio(
                                value=color,
                                fill_color=color, 
                                tooltip=color.title()
                            )
                            for color in THEME_COLORS
                        ]
                    ),
                    on_change=lambda e: ThemeController.set_theme_color(e.data, self.page)
                ),
                ft.IconButton(
                    on_click=lambda e: ThemeController.toggle_theme_mode(self.page)
                )
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )

        self.set_theme_mode_icon()

    def on_window_resize(self, e: ft.WindowResizeEvent):
        control = self.content.controls[1].content
        control.width = min(555, e.width - 150)
        control.update()

    def set_theme_mode_icon(self) -> None:
        saved_mode = self.page.client_storage.get("theme_mode") or self.page.platform_brightness.name.lower()
        icon = ("light" if saved_mode == "dark" else "dark") + "_mode"
        self.content.controls[-1].icon = icon

    def open_about_dialog(self, e: ft.ControlEvent) -> None:
        about = About(self.page)
        self.page.open(about)
