import flet as ft


class PageController:

    def __init__(self, page: ft.Page):
        self.page = page
        self.game_theme = ""
        self.game_location = ""
        self.player_name = ""
        

    def get_prompts(self):
        print("made it here")
        self.game_theme = self.tf1.value
        self.game_location = self.tf2.value
        self.player_name = self.tf3.value
        print("Game Theme: " + self.game_theme)
        print("Game Location: " + self.game_location)
        print("Player Name: " + self.player_name)

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
            c1 = ft.Container(
                            content=ft.Text(
                                value="What type of adventure would you like to have?",
                                style=ft.TextThemeStyle.HEADLINE_SMALL,
                            ),
                            padding=5,
                        )
            tf1 = ft.TextField(
                                hint_text="For example: A fantasy role-playing game, a sci-fi adventure, etc.",
                            )
            self.tf1 = tf1
            c2 = ft.Container(
                            content=tf1,
                            padding=5,
                            margin = ft.margin.only(bottom=30)
                        )
            c3 = ft.Container(
                            content=ft.Text(
                                value="Where will your adventure take place?",
                                style=ft.TextThemeStyle.HEADLINE_SMALL,
                            ),
                            padding=5,
                            margin = ft.margin.only(top=25)
                        )
            tf2 = ft.TextField(
                                hint_text="For example: A castle, a spaceship, etc.",
                            )
            self.tf2 = tf2
            c4 = ft.Container(
                            content=tf2,
                            padding=5,
                            margin = ft.margin.only(bottom=30)
                        )
            c5 = ft.Container(
                            content=ft.Text(
                                value="What is your character's name?",
                                style=ft.TextThemeStyle.HEADLINE_SMALL,
                            ),
                            padding=5,
                            margin = ft.margin.only(top=25)
                        )
            tf3 = ft.TextField(
                                hint_text="For example: John Smith, Captain Kirk, etc.",
                            )
            c6 = ft.Container(
                            content=tf3,
                            padding=5,
                        )
            self.tf3 = tf3
            self.page.views.append(
                ft.View(
                    "/prompts",
                    [
                        c1,
                        c2,
                        c3,
                        c4,
                        c5,
                        c6,
                        ft.Container(
                            content=ft.ElevatedButton(
                                text="Play!",
                                style=ft.ButtonStyle(
                                    shape=ft.RoundedRectangleBorder(radius=10),
                                    overlay_color=ft.colors.BLACK12,
                                    bgcolor=ft.colors.WHITE,
                                    color=ft.colors.BLACK,
                                ),
                                on_click=lambda _: self.get_prompts(),
                            ),
                            padding=5,
                            margin = ft.margin.only(top=30)
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