#!/usr/bin/python3
# -*- coding: utf-8 -*-

import base64
import flet as ft

from ..model.client_storage import ClientStorage
from ..view.account_image import YAccountImage
from ..view.new_account_dialog import YNewAccountDialog


class YCaptchaVerifyDialog(ft.AlertDialog):
    def __init__(self, page: ft.Page):
        super().__init__()

        self._page = page
        self._client_storage = ClientStorage(self._page)

        self.modal = True
        self.title = ft.Text(text_align="center")
        self.actions_alignment = ft.MainAxisAlignment.END

        self.captcha_update = ft.Ref[ft.IconButton]()

        self.account_image = YAccountImage()
        self.account_name = ft.Text()
        self.captcha_image = ft.Image(fit=ft.ImageFit.FILL)

        self.captcha_value = ft.TextField(
            input_filter=ft.InputFilter(r"[0-9]"),
            text_align="center",
            max_length=4,
            suffix=ft.IconButton(
                ref=self.captcha_update,
                icon = ft.icons.REFRESH
            )
        )

        self.icon = ft.Column(
            controls=[
                self.account_image,
                self.account_name
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

        self.content = ft.Column(
            controls=[
                self.captcha_image,
                self.captcha_value
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

        self.actions = [
            ft.ElevatedButton(
                data=1,
                text = "تحقق"
            ), # Yes
            ft.ElevatedButton(
                data=0,
                text = "الغاء", 
                on_click=lambda e: self._page.close(self)
            )  # Cancel
        ]

    def set_captcha_image(self, captcha: bytes):
        self.captcha_image.src_base64 = base64.b64encode(captcha).decode()

    def open_dialog(self, 
                    atype: int | str, 
                    username: str,
                    captcha: bytes):

        self.captcha_value.value = ""

        self.title.value = self._client_storage.get_user_data_key(atype, username, "name") or username
        self.account_name.value = YNewAccountDialog._names[int(atype)]
        self.set_captcha_image(captcha)
        self.account_image.set_image(int(atype))

        self._page.open(self)
        self.update()