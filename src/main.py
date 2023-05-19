import flet as ft
from PageController import PageController


def main(page: ft.Page):
    page.theme_mode = "DARK"
    page.vertical_alignment = "CENTER"
    page.horizontal_alignment = "CENTER"
    page.title = "A Text-Based Adventure"
    page.window_width = 600
    page.window_height = 800
	
    page_controller = PageController(page)

    def route_change(route):
        page_controller.route_change(route)

    def view_pop(view):
        page_controller.view_pop(view)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)


# ft.app(target=main, view=ft.WEB_BROWSER)
ft.app(target=main)
