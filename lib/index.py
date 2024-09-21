
import flet as ft

from .views.card import Card
from .models.user import User
from .views.user_new import UserViewNew
from .views.list_user import UserListView
from .views.bottom_bar import BottomAppBar
from .constant import Refs, REFRESH_ARROWS, ThemeController


class ProgressRing(ft.ProgressRing):
    def __init__(self, **kwargs):
        super().__init__(ref=Refs.loader, **kwargs)

        self.width = 18
        self.height = 18
        self.visible = False

    def show(self) -> None:
        self.visible = True
        self.update()
    
    def hide(self) -> None:
        self.visible = False
        self.update()


class Application:

    def open_user_view_new(self, e: ft.ControlEvent):
        user_view_new = UserViewNew(self.page)
        self.page.open(user_view_new)

    def on_close_window(self, e = None):
        self.page.client_storage.set("size", [self.page.window.width, self.page.window.height])

    def __call__(self, page: ft.Page) -> None:
        self.page = page

        page.window.wait_until_ready_to_show = True

        page.title = "الاستعلام عن رصيد يمن نت"
        page.window.icon = "assets/icon.png"
        page.theme_mode = page.client_storage.get("theme_mode") or page.platform_brightness.name.lower()

        page.padding = ft.padding.only(top=35)
        page.expand = True

        if page.platform not in (ft.PagePlatform.ANDROID, ft.PagePlatform.IOS):
            page.on_close = self.on_close_window

            page.window.min_width = 330
            page.window.min_height = 600

            page.window.max_width = 600
            page.window.max_height = 700
            
            if page.client_storage.contains_key("size"):
                page.window.width = page.client_storage.get("size")[0]
                page.window.height = page.client_storage.get("size")[1]

        page.horizontal_alignment = page.vertical_alignment = "center"
        page.fonts = {
            "linaround": "assets/fonts/linaround_regular.otf"
        }

        ThemeController.set_theme_color(page.client_storage.get("theme_color") or "INDIGO", page)

        controls = [
            ft.Column(
                expand=True,
                controls=[
                    ft.Stack(
                        controls=[
                            ft.Container(
                                ref=Refs.header,
                                padding=0,
                                margin=0,
                                # height=page.window.height - (page.window.height / 2 + page.window.height / 6.6),
                                height=230,
                                border_radius=ft.BorderRadius(0, 0, 42, 42),
                                bgcolor=page.theme.color_scheme_seed
                            ),
                            ft.Container(
                                expand=True,
                                content=ft.Row(
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    controls=[
                                        ft.Text(
                                            ref=Refs.refresh_text,
                                            value = "اسحب للأسفل للتحديث" + REFRESH_ARROWS[0],
                                            size=11,
                                            rtl=True,
                                            text_align="center",
                                            color=ft.colors.WHITE
                                        ),
                                        ProgressRing()
                                    ]
                                ),
                                alignment=ft.alignment.center,
                                # margin=ft.margin.only(top=10)
                            ),
                            Card(page)
                        ]
                    ),
                    UserListView()
                ]
            )
        ]

        page.bottom_appbar = BottomAppBar(page)
        page.floating_action_button_location = ft.FloatingActionButtonLocation.CENTER_DOCKED
        page.floating_action_button = ft.FloatingActionButton(
            icon=ft.icons.ADD,
            mini=True,
            on_click=self.open_user_view_new
        )

        page.add(*controls)

        if User.get_users() and (user := User.get_users()[0]).data is not None:
            Refs.card.current.set_data(user.id, True)

if __name__ == "__main__":
    ft.app(target=Application())