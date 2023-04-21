import flet as ft
from Routing import Routing


def main(page: ft.Page):
    page.theme_mode = "DARK"
    page.vertical_alignment = "CENTER"
    page.horizontal_alignment = "CENTER"
    page.title = "A Text-Based Adventure"
    page.window_width = 600
    page.window_height = 800

    route_handler = Routing(page)

    def route_change(route):
        route_handler.route_change(route)

    def view_pop(view):
        route_handler.view_pop(view)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)


ft.app(target=main)
