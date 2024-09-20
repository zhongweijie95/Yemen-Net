#!/usr/bin/python3
# -*- coding: utf-8 -*-

import flet as ft
from humanize import naturalsize


USERNAME = "omamkaz"
REFRESH_ARROWS = ("⭭", "⇡")
ACCOUNT_TYPES = ("Yemen Net (ADSL)", "4G LTE", "Phone")
ABOUT_LINK_ICONS = (
    ("google", "#db4437", f"mailto:{USERNAME}@gmail.com"),
    ("paypal", "#00a7ce", f"PayPal.me/{USERNAME}"),
    ("telegram", "#0088cc", f"https://t.me/{USERNAME}"),
    ("whatsapp", "#25d366", "https://wa.me/967776973923"),
    ("github", "#000000", f"https://www.github.com/{USERNAME}"),
    ("twitter", "#1da1f2", f"https://www.twitter.com/{USERNAME}"),
    ("facebook", "#1877f2", f"https://www.facebook.com/{USERNAME}")
)
THEME_COLORS = (
    "INDIGO", "AMBER", "BLUE", 
    "BROWN", "CYAN", "GREEN", 
    "GREY", "LIME", "ORANGE", 
    "PINK", "PURPLE", "RED", 
    "TEAL", "YELLOW"
)

class UserData:

    @staticmethod
    def custom_credit(value: str | float | int) -> str:
        return naturalsize(float(value) * 10**9, format="%.2f")

    @classmethod
    def filter_data(cls, data: dict[str, str], atype: int | str) -> dict[str, str]:
        return getattr(cls, f"type_{atype}")(data)

    @classmethod
    def type_0(cls, data: dict[str, str]) -> dict[str, str]:
        for k, v in data.items():
            if isinstance(v, str) and "جيجابايت" in v:
                u, _ = v.strip().split()
                v = UserData.custom_credit(u.strip())
                data[k] = v
        return data

    @classmethod
    def type_1(cls, data: dict[str, str]) -> dict[str, str]:
        return data

    @classmethod
    def type_2(cls, data: dict[str, str]) -> dict[str, str]:
        for k, v in data.items():
            if "gb" in k.lower():
                u, _ = v.split()
                v = UserData.custom_credit(u.strip())
                data[k] = v
        return data


class Refs:
    card = ft.Ref[ft.Container]()
    header = ft.Ref[ft.Container]()
    refresh_text = ft.Ref[ft.Text]()
    user_list = ft.Ref[ft.ListView]()
    loader = ft.Ref[ft.ProgressRing]()


class ThemeController:

    @staticmethod
    def toggle_theme_mode(page: ft.Page) -> None:
        page.bottom_appbar.content.controls[-1].icon = page.theme_mode + "_mode"
        page.theme_mode = "light" if page.theme_mode == "dark" else "dark"
        page.client_storage.set("theme_mode", page.theme_mode)
        page.update()

    @staticmethod
    def set_theme_color(color: str, page: ft.Page) -> None:
        page.theme = page.dark_theme = ft.Theme(
            color_scheme_seed=color,
            use_material3=True,
            font_family="linaround",
            primary_color=color + "900",
            divider_theme=ft.DividerTheme(
                color = color + "900"
            )
        )

        if Refs.card.current is not None:
            Refs.card.current.content.bgcolor = color + "800"
            Refs.card.current.update()

        if Refs.header.current is not None:
            Refs.header.current.bgcolor = color
            Refs.header.current.update()

        page.client_storage.set("theme_color", color)
        page.update()
