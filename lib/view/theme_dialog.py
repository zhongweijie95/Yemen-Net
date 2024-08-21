#!/usr/bin/python3
# -*- coding: utf-8 -*-

import flet as ft


class YThemeModeSelect(ft.BottomSheet):
    def __init__(self, page: ft.Page):
        super().__init__(ft.Control)

        self._page = page

        self.content = ft.RadioGroup(
            value = page.client_storage.get("theme.mode") or "system",
            content=ft.Container(
                content=ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_AROUND,
                    controls=[
                        ft.Column(
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER, 
                            controls=[
                                ft.Image(src=f"assets/{theme}.png", width=64, height=64, filter_quality=ft.FilterQuality.HIGH),
                                ft.Text(value=theme.title()), 
                                ft.Radio(value=theme)
                            ]
                        )
                        for theme in ("system", "dark", "light")
                    ]
                ),
                margin=ft.margin.only(top=30)
            ),
            on_change=self.change_theme_mode
        )

    def change_theme_mode(self, e: ft.ControlEvent) -> None:
        mode: str = e.control.value

        self._page.client_storage.set("theme.mode", mode)
        self._page.theme_mode = ft.ThemeMode(mode)
        self._page.update()