import flet as ft


def main(page: ft.Page):
    page.theme_mode = "DARK"
    page.vertical_alignment = "CENTER"
    page.horizontal_alignment = "CENTER"
    page.title = "A Text-Based Adventure"
    page.window_width = 600
    page.window_height = 800

    def begin_clicked(e):
        page.go("/store")
        print("Clicked!")

    def route_change(route):
        page.views.clear()
        page.views.append(
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
                            on_click=lambda _: page.go("/prompts"),
                        ),
                        padding=5,
                    ),
                ],
                vertical_alignment = "CENTER",
                horizontal_alignment = "CENTER"
            )
        )

        if page.route == "/prompts":
            page.views.append(
                ft.View(
                    "/prompts",
                    [
                        ft.ElevatedButton(
                            "Go Home", on_click=lambda _: page.go("/")
                        ),
                    ],
                    vertical_alignment = "CENTER",
                    horizontal_alignment = "CENTER"
                )
            )
        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)


ft.app(target=main)
