#!/usr/bin/python3
# -*- coding: utf-8 -*-

import requests
import flet as ft

from .captcha_verify import CaptchaVerify
from ..scrapper import YADSL, LTE, Phone, ParserError
from ..constant import Refs, REFRESH_ARROWS, UserData
from ..models.user import User


class CardItem(ft.Container):
    def __init__(self, 
                 label: str, 
                 value: str,
                 end: bool = False,
                 **kwargs):
        super().__init__(**kwargs)

        self.margin=0
        self.padding = ft.padding.only(left=10, right=10)
        self.content = ft.Column(
            spacing=0,
            controls=[
                ft.Row(
                    spacing=0,
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Text(
                            value=value,
                            color=ft.colors.WHITE,
                            size=11,
                            text_align="left",
                            weight=ft.FontWeight.W_500,
                            overflow=ft.TextOverflow.CLIP,
                            font_family="circle_rounded",
                            selectable=True
                        ),
                        ft.Text(
                            value=label,
                            color=ft.colors.WHITE,
                            size=14,
                            font_family="linaround",
                            text_align="right"
                        )
                    ]
                )
            ]
        )

        if not end:
            self.content.controls.append(
                ft.Divider(
                    leading_indent=4,
                    trailing_indent=4
                )
            )
        else:
            self.margin = ft.margin.only(bottom=10)

    def hide_line(self) -> None:
        self.content.controls[-1].visible = False
        self.update()

    def show_line(self) -> None:
        self.content.controls[-1].visible = True
        self.update()

    def _set_item_value(self, index: int, value: str) -> None:
        c = self.content.controls[0].controls[index]
        c.value = value
        self.update()

    def set_label(self, label: str):
        self._set_item_value(1, label)

    def set_value(self, value: str):
        self._set_item_value(0, value)


class CardTitle(ft.ListTile):
    def __init__(self):
        super().__init__()

        self.content_padding = ft.padding.only(right=10)
        self.title = ft.Text(
            size=14.5,
            color=ft.colors.WHITE,
            text_align="right"
        )
        self.subtitle = ft.Text(
            text_align="right",
            color=ft.colors.WHITE70,
            size=14
        )
        self.trailing = ft.Stack(
            alignment=ft.alignment.bottom_right,
            controls=[
                ft.Image(
                    src="assets/atype/0.png",
                    width=42,
                    height=42
                ),
                ft.Badge(
                    bgcolor=ft.colors.GREEN,
                    small_size=13,
                    alignment=ft.alignment.bottom_right
                )
            ]
        )

    def set_active(self, on: bool = True) -> None:
        self.trailing.controls[-1].bgcolor = "green" if on else "red"
        self.update()

    def set_logo(self, atype: int | str) -> None:
        self.trailing.controls[0].src = f"assets/atype/{atype}.png"
        self.update()

    def set_title(self, title: str) -> None:
        self.title.value = title
        self.update()

    def set_subtitle(self, subtitle: str) -> None:
        self.subtitle.value = subtitle
        self.update()


class CardCredit(ft.Container):
    def __init__(self):
        super().__init__()

        self.padding = 0
        self.margin = 0
        self.expand = True
        self.content = ft.Column(
            spacing=6,
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text(
                    value="الرصيد المتاح",
                    color=ft.colors.WHITE,
                    size=14,
                    rtl=True
                ),
                ft.Text(
                    color = ft.colors.WHITE,
                    # font_family="circle_rounded",
                    font_family="Monospace",
                    size = 18,
                    weight=ft.FontWeight.W_700,
                    spans=[
                        ft.TextSpan(
                            style = ft.TextStyle(
                                size = 14,
                                color = ft.colors.GREEN
                            ),
                            visible=False
                        )
                    ]
                )
            ]
        )

    def hide_credit_state(self):
        self.content.controls[-1].spans[0].visible = False

    def _credit_state(self, value: str, color: str, prefix: str) -> None:
        span = self.content.controls[-1].spans[0]
        span.style.color = color
        span.text = (" " * 3) + f"{prefix}{value}"
        span.visible = True

        span.update()
        self.update()

    def increment(self, value: str) -> None:
        self._credit_state(value, "green", "+")

    def decrement(self, value: str) -> None:
        self._credit_state(value, "red", "-")

    def set_credit(self, value: str):
        credit = self.content.controls[-1]
        credit.value = value
        self.update()


class Card(ft.GestureDetector):
    _user_id: int = None

    def __init__(self, page: ft.Page, **kwargs):
        super().__init__(ref=Refs.card, **kwargs)

        self.page = page

        self.card_title: CardTitle = CardTitle()
        self.card_credit: CardCredit = CardCredit()

        self.card_title.visible = False
        self.card_credit.visible = False

        self.on_pan_end = self._on_pan_end
        self.on_pan_start = self._on_pan_start
        self.on_pan_update = self._on_pan_update

        self.content = ft.Container(
                expand=True,
                padding=0,
                margin=ft.margin.only(left=12, right=12, top=35),
                height=320,
                border_radius=14,
                alignment=ft.alignment.center,
                animate=ft.Animation(200, ft.AnimationCurve.LINEAR_TO_EASE_OUT),
                bgcolor=self.page.theme.color_scheme_seed + "800",
                shadow=ft.BoxShadow(
                    spread_radius=-10,
                    blur_radius=8,
                    color=ft.colors.with_opacity(ft.colors.BLACK, 0.07),
                    offset=ft.Offset(0, 8)
                ),
                content = ft.Column(
                    spacing=0,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        # Icon, and Name title
                        self.card_title,
                        # Balance
                        self.card_credit
                    ]
                )
            )
        
        for i in range(5):
            self.content.content.controls.append(
                CardItem("", "", i == 4, visible=False)
            )

    def reset_items(self):
        for i in range(5):
            i += 2
            c = self.content.content.controls[i]
            c.visible = False
        self.content.content.update()

    def set_card_items(self, data: dict[str, str]) -> None:
        for index, (label, value) in enumerate(data.items()):
            index += 2
            if index <= (4 + 2):
                c = self.content.content.controls[index]
                c.visible = True

                c.set_label(label)
                c.set_value(value)

    def _calc_old_data(self, old_data: dict[str, str]) -> None:
        def get_value(var):
            return float(var.get("valid_credit").split()[0].strip())

        if old_data:
            old_value = get_value(old_data)
            new_value = get_value(self._user.data)

            if new_value < old_value:
                self.card_credit.decrement(UserData.custom_credit(old_value - new_value))
            elif new_value != old_value:
                self.card_credit.increment(UserData.custom_credit(new_value))

    def _set_fetch_data(self, old_data: dict[str, str] = None):
        # if self._user.atype != 2:
        #     self.expand_card()
        # else:
        #     self.collapse_card()

        self.card_title.visible = True
        self.card_credit.visible = True
        self.card_credit.hide_credit_state()

        self.reset_items()

        pdata = UserData.filter_data(self._user.data.copy(), self._user.atype)

        if self._user.atype == 2:
            self.card_title.set_title(self._user.username)
            self.card_title.set_subtitle(self._user.dname)
            self.card_title.set_logo(self._user.atype)
            self.card_credit.visible = False
            self.set_card_items(pdata)

        elif self._user.atype == 1:

            self.card_title.set_title(self._user.username)
            self.card_title.set_subtitle(self._user.dname)
            self.card_title.set_logo(self._user.atype)

            self.card_credit.set_credit(pdata.pop("valid_credit"))
            self._calc_old_data(old_data)
            self.set_card_items(pdata)

        else:

            self.card_title.set_logo(self._user.atype)
            self.card_title.set_title(pdata.pop("name"))
            self.card_credit.set_credit(pdata.pop("valid_credit"))
            self._calc_old_data(old_data)

            self.card_title.set_active(pdata.pop("account_status"))
            self.card_title.set_subtitle(self._user.username)

            for index, (label, value) in enumerate(pdata.items()):
                index = index + 2
                if index <= (4 + 2):
                    c = self.content.content.controls[index]
                    c.visible = True
                    c.set_label(label)
                    c.set_value(value)

        self.update()

    def _fetch_data(self):
        Refs.loader.current.show()

        isp = (YADSL, LTE, Phone)[self._user.atype]()

        old_data = self._user.data.copy() if self._user.data is not None else {}
        new_data = isp.fetch_data(self._user.cookies)

        User.edit_data_and_cookies(self._user_id, new_data, isp.get_cookies())
        self._set_fetch_data(old_data)

        Refs.loader.current.hide()

    def _login(self):
        isp = (YADSL, LTE, Phone)[self._user.atype]()

        def on_submit(data: dict[str, str], old_data: dict[str, str] = None):
            if self._user.atype != 0:
                # cookies = None if self._user.atype != 0 else isp.get_cookies()
                User.edit_data_and_cookies(self._user_id, data, None)
                self._set_fetch_data(old_data)
            else:
                User.edit_data_and_cookies(self._user_id, data, isp.get_cookies())
                self._set_fetch_data(old_data)
                # self._fetch_data()

        try:
            if self._user.atype != 0:
                old_data = self._user.data
                isp.login(self._user.username)
                cv = CaptchaVerify(self.page, isp, lambda data: on_submit(data, old_data), 5)
                cv.open_dialog()
            else:
                self._fetch_data()
        except AttributeError:
            isp.login(self._user.username, self._user.password)
            cv = CaptchaVerify(self.page, isp, on_submit, 5 if self._user.atype != 0 else 4)
            cv.open_dialog()
        except requests.exceptions.ConnectionError:
            # No Internet Connection
            self.page.open(
                ft.AlertDialog(
                    icon=ft.Icon(ft.icons.WIFI_OFF, ft.colors.RED),
                    content=ft.Text(
                        rtl=True,
                        value = "لايوجد اتصال انترنت!",
                        text_align="center"
                    )
                )
            )
        except (Exception, ParserError) as err:
            self.page.open(
                ft.AlertDialog(
                    icon=ft.Icon(ft.icons.ERROR, ft.colors.RED),
                    content=ft.Text(
                        value = str(err),
                        text_align="center"
                    )
                )
            )

        Refs.loader.current.hide()

    def set_data(self, user_id: int, display: bool = False) -> None:
        if self._user_id != user_id:
            self._user_id = user_id

        if self._user.data is not None:
            self._set_fetch_data()
        elif not display:
            self._login()

    def _on_pan_update(self, e: ft.DragUpdateEvent) -> None:
        if self.content.margin.top < (35 + 8) and e.delta_y >= 0:
            self.content.margin.top += min(0.5, e.delta_y) * 5
            self.content.update()

    def _on_pan_end(self, e: ft.DragEndEvent) -> None:
        self.content.margin.top = 35
        self.content.update()

        Refs.refresh_text.current.value = Refs.refresh_text.current.value.replace(*REFRESH_ARROWS[::-1])
        Refs.refresh_text.current.update()

        if self._user_id is not None:
            self._login()
        elif len(User.get_users()) > 0:
            self.set_data(User.get_users()[0].id)

    def _on_pan_start(self, e: ft.DragStartEvent) -> None:
        Refs.refresh_text.current.value = Refs.refresh_text.current.value.replace(*REFRESH_ARROWS)
        Refs.refresh_text.current.update()

    @property
    def _user(self):
        return User.get_user(self._user_id)
