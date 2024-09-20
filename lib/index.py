
import flet as ft

from .views.card import Card
# from .models.base import Session
from .models.base import Engine
from .views.user_new import UserViewNew
from .views.list_user import UserListView
from .viewmodels.user_vm import UserViewModel
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

    def __call__(self, page: ft.Page) -> None:
        self.page = page

        self.vm = UserViewModel()

        page.title = "الاستعلام عن رصيد يمن نت"
        page.theme_mode = page.client_storage.get("theme_mode") or page.platform_brightness.name.lower()
        page.window.icon = "assets/icon.png"

        page.padding = 0
        page.expand = True

        if page.platform not in (ft.PagePlatform.ANDROID, ft.PagePlatform.IOS):
            page.window.min_width = 330
            page.window.min_height = 600

            page.window.max_width = 600
            page.window.max_height = 700

        page.window.wait_until_ready_to_show = True
        page.horizontal_alignment = page.vertical_alignment = "center"
        page.on_close = lambda e: Engine.session().close_all()
        page.fonts = {
            "linaround": "assets/fonts/linaround_regular.otf"
        }

        ThemeController.set_theme_color(page.client_storage.get("theme_color") or "INDIGO", page)

        controls = [
            ft.Stack(
                expand=True,
                controls=[
                    ft.Column(
                        controls=[
                            ft.Stack(
                                controls=[
                                    ft.Container(
                                        ref=Refs.header,
                                        padding=0,
                                        margin=0,
                                        height=page.window.height - (page.window.height / 2 + page.window.height / 6.6),
                                        border_radius=ft.BorderRadius(0, 0, 42, 42),
                                        bgcolor=page.theme.color_scheme_seed
                                    ),
                                    ft.Container(
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
                                        margin=ft.margin.only(top=10)
                                    ),
                                    Card(page)
                                ]
                            ),
                            UserListView()
                        ]
                    )
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

        if self.vm.users and (user := self.vm.users[0]).data is not None:
            Refs.card.current.set_data(user.id, True)

if __name__ == "__main__":
    ft.app(target=Application())