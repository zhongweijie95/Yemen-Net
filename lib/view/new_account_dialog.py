#!/usr/bin/python3
# -*- coding: utf-8 -*-

import flet as ft
from .account_image import YAccountImage


class YNewAccountDialog(ft.AlertDialog):
    _names = ('Yemen Net (ADSL)', '4G LTE', 'Phone')

    def __init__(self, page: ft.Page):
        super().__init__()

        self._page = page
        self._index: int = 0

        self.modal = True
        self.title = ft.Text("اضافة حساب جديد", text_align="center")
        self.actions_alignment = ft.MainAxisAlignment.END

        self.icon = ft.IconButton(
            content=ft.Column(
                controls=[
                    YAccountImage(0),
                    ft.Text(self._names[0])
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
            on_click=self.handle_open_bottom_sheet
        )

        self.bottom_sheet = ft.BottomSheet(
            content=ft.Column(
                spacing=10,
                controls=[
                    ft.ListTile(
                        data = index,
                        leading = YAccountImage(index),
                        title = ft.Text(self._names[index]),
                        on_click = self.handle_index_changed,
                        disabled=index != 0
                    )
                    for index in range(3)
                ]
            )
        )

        self.display_name = ft.TextField(
            text_align = "center",
            label = "الاسم المستعار",
            max_length = 24
        )

        self.username = ft.TextField(
            text_align="center",
            label="أسم المستخدم",
            input_filter=ft.InputFilter(r"[a-zA-Z0-9]+"),
        )

        self.password = ft.TextField(
            text_align="center",
            label="كلمة السر",
            password=True,
            can_reveal_password=True,
            input_filter=self.username.input_filter
        )

        self.actions = [
            ft.ElevatedButton(text = "اضافة", data=1), # Yes
            ft.ElevatedButton(text = "الغاء", data=0)  # Cancel
        ]

        self.content = ft.Column(
            controls=[
                self.display_name,
                self.username,
                self.password
            ]
        )

    def clear_forms(self):
        self.display_name.value = ""
        self.username.value = ""
        self.password.value = ""
        self.update()

    def handle_open_bottom_sheet(self, e: ft.ControlEvent) -> None:
        self._page.open(self.bottom_sheet)

    def handle_index_changed(self, e: ft.ControlEvent) -> None:
        self._index = e.control.data

        self.password.visible = not self._index
        self.icon.content.controls[0].set_image(self._index)
        self.icon.content.controls[1].value = (self._names[self._index])

        self._page.close(self.bottom_sheet)

        self.update()