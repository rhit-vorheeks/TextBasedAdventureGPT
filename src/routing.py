import flet as ft


class Routing:

    def __init__(self, page: ft.Page):
        self.page = page
        self.game_theme = ""
        self.game_location = ""
        self.player_name = ""

    def get_prompts(self):
        # TODO: get prompts from the text boxes
        return 0

    def route_change(self, route):
        self.page.views.clear()
        self.page.views.append(
            ft.View(
                "/",
                [
                    ft.Container(
                        content=ft.Text(
                            value="A Simple Text-Based Adventure!",
                            style=ft.TextThemeStyle.HEADLINE_SMALL,
                        ),
                        padding=20,
                    ),
                    ft.Container(
                        content=ft.ElevatedButton(
                            text="Begin!",
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=10),
                                overlay_color=ft.colors.BLACK12,
                                bgcolor=ft.colors.WHITE,
                                color=ft.colors.BLACK,
                            ),
                            on_click=lambda _: self.page.go("/prompts"),
                        ),
                        padding=5,
                    ),
                ],
                vertical_alignment = "CENTER",
                horizontal_alignment = "CENTER"
            )
        )

        if self.page.route == "/prompts":
            self.page.views.append(
                ft.View(
                    "/prompts",
                    [
                        ft.ElevatedButton(
                            "Go Home", on_click=lambda _: self.get_prompts()
                        ),
                    ],
                    vertical_alignment = "CENTER",
                    horizontal_alignment = "CENTER"
                )
            )
        self.page.update()

    def view_pop(self, view):
        self.page.views.pop()
        top_view = self.page.views[-1]
        self.page.go(top_view.route)