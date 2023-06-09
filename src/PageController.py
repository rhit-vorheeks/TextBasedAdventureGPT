import flet as ft
from GPTController import GPTController
from GameDataController import GameDataController
from GameController import GameController
from time import sleep
from NPC import Npc


class PageController:
    def __init__(self, page: ft.Page):
        self.page = page
        self.gpt_controller = GPTController()
        self.game_data_controller = GameDataController()
        self.sent_message = False

    def get_prompts(self):
        self.game_data_controller.set_game_theme(self.tf1.value)
        self.game_data_controller.set_game_location(self.tf2.value)
        self.game_data_controller.set_player_name(self.tf3.value)
        # self.game_data_controller.generate_game_dataset()
        
        self.page.go("/loading")

        # TODO: DO LOADING HERE
        self.game_data_controller.generate_game_dataset(self.progress_bar, self.page)
        # self.testNPC = Npc()
        # self.testNPC.setup_npc(self.game_data_controller.get_game_theme(), self.game_data_controller.get_game_location(), self.game_data_controller.get_player_name(), "", "", "")
        self.game_controller = GameController(self.game_data_controller, self)
        self.page.go("/game")

    def setup_prompt(self):
        c1 = ft.Container(
            content=ft.Text(
                value="What type of adventure would you like to have?",
                style=ft.TextThemeStyle.HEADLINE_SMALL,
            ),
            padding=5,
        )
        tf1 = ft.TextField(
            hint_text="For example: A fantasy role-playing game, a sci-fi adventure, etc.",
            border_color=ft.colors.WHITE70,
        )
        self.tf1 = tf1
        c2 = ft.Container(content=tf1, padding=5, margin=ft.margin.only(bottom=30))
        c3 = ft.Container(
            content=ft.Text(
                value="Where will your adventure take place?",
                style=ft.TextThemeStyle.HEADLINE_SMALL,
            ),
            padding=5,
            margin=ft.margin.only(top=25),
        )
        tf2 = ft.TextField(
            hint_text="For example: A castle, a spaceship, etc.",
            border_color=ft.colors.WHITE70,
        )
        self.tf2 = tf2
        c4 = ft.Container(content=tf2, padding=5, margin=ft.margin.only(bottom=30))
        c5 = ft.Container(
            content=ft.Text(
                value="What is your character's name?",
                style=ft.TextThemeStyle.HEADLINE_SMALL,
            ),
            padding=5,
            margin=ft.margin.only(top=25),
        )
        tf3 = ft.TextField(
            hint_text="For example: John Smith, Captain Kirk, etc.",
            border_color=ft.colors.WHITE70,
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
                        margin=ft.margin.only(top=30),
                    ),
                ],
                vertical_alignment="CENTER",
                horizontal_alignment="CENTER",
            )
        )

    # def send_message_click(self, e, new_message):
    #     if new_message.value != "":
    #         the_new_message = new_message.value.strip()
    #         new_message.value = ""
    #         # add read only flag swap here.
    #         new_message.read_only = True
    #         self.add_message(the_new_message, True, "", False)
    #         new_message.read_only = False
    #         new_message.focus()
    #         self.page.update()

    def add_message(self, message, is_player, npc, is_game_text):
        # npc = self.testNPC # remove later
        text_message = ft.Text(value="", selectable=True)
        progress_bar = ft.ProgressRing(
            width=16,
            height=16,
            stroke_width=2,
            tooltip="Waiting for response...",
        )
        container = ft.Container(
            content=progress_bar,
            padding=ft.padding.symmetric(horizontal=7),
            margin=ft.margin.only(bottom=5)
        )
        the_name = ""
        if is_player:
            the_name = self.game_data_controller.get_player_name()
        elif is_game_text:
            the_name = "Game"
        else:
            the_name = npc.get_name()
        column = ft.Column(
            [
                ft.Text(
                    value=the_name,
                    weight="bold",
                ),
                text_message,
                container,
            ],
            spacing=0,
        )
        m = ft.ResponsiveRow(
            vertical_alignment="start",
            controls=[column],
        )

        self.chat.controls.append(m)
        self.page.update()

        if is_player:
            container.visible = False
            progress_bar.visible = False
            text_message.value = message
            self.page.update()
            # self.add_message(message, False, "GPT", False)
        else:
            # message = self.gpt_controller.get_description(
            #     "You are pretending to be a human, act helpful and be clever/funny. respond to the person '"
            #     + self.game_data_controller.get_player_name()
            #     + "' who told you only '"
            #     + message + "'"
            # ).strip()

            #TODO UNCOMMENT THIS AND FIX IT SO IT PASSES IN THE PROMPT AND CALLS HERE, NOT IN ROOM
            if (npc != False):
                message = npc.response(message)
            progress_bar.visible = False
            container.visible = False
            self.page.update()
            placeholder_text = ft.Text(value=" ")
            placeholder_column = ft.Column(
                [
                   placeholder_text
                ],
                spacing=100,
            )
            placeholder = ft.ResponsiveRow(
                vertical_alignment="start",
                controls=[placeholder_column],
            )
            self.chat.controls.append(placeholder)
            for character in message:
                text_message.value += character

                self.page.update()
                sleep(0.005)
            
            self.chat.controls.pop()

        self.page.update()

    def wait_for_input(self):
        self.new_message.read_only = False
        while(self.sent_message == False):
            sleep(0.1)
        self.sent_message = False
        self.new_message.read_only = True
        return self.the_new_message


    def setup_loading(self):
        print("loading")
        self.progress_bar = ft.ProgressRing(
            width=64,
            height=64,
            stroke_width=4,
            value=0,
            tooltip="Generating Game...",
        )
        # progress_container = ft.Container(
        #     content=progress_bar,
        #     padding=ft.padding.symmetric(horizontal=7),
        #     margin=ft.margin.only(bottom=5)
        # )
        self.page.views.append(
            ft.View(
                "/loading",
                [
                    ft.Container(
                        content=ft.Text(
                            value="Currently generating your experience!",
                            style=ft.TextThemeStyle.HEADLINE_SMALL,
                        ),
                        padding=50,
                    ),
                    self.progress_bar
                ],
                # horizontal_alignment="CENTER",
                vertical_alignment="CENTER",
                horizontal_alignment="CENTER",
            )
        )

    def message_entered(self, new_message):
        if new_message.value != "":
            self.the_new_message = new_message.value.strip()
            self.sent_message = True
            new_message.value = ""
            # add read only flag swap here.
            # new_message.read_only = True
            # self.add_message(the_new_message, True, "", False)
            # new_message.read_only = False
            new_message.focus()
            self.page.update()

    def setup_game(self):
        self.chat = ft.Column()
        new_message = ft.TextField()

        self.chat = ft.ListView(
            expand=True,
            spacing=10,
            auto_scroll=True,
        )

        # call_send_message_click = lambda e: self.send_message_click(
        #     e, new_message, self.chat
        # )

        self.new_message = new_message
        call_send_message_click = lambda e: self.message_entered(new_message)

        new_message.read_only = True
        new_message = ft.TextField(
            hint_text="Write a message...",
            autofocus=True,
            shift_enter=True,
            min_lines=1,
            max_lines=5,
            filled=True,
            expand=True,
            on_submit=call_send_message_click,
        )

        self.page.views.append(
            ft.View(
                "/game",
                [
                    ft.Container(
                        content=self.chat,
                        border=ft.border.all(1, ft.colors.OUTLINE),
                        border_radius=5,
                        padding=10,
                        expand=True,
                    ),
                    ft.Row(
                        [
                            new_message,
                            ft.IconButton(
                                icon=ft.icons.SEND_ROUNDED,
                                tooltip="Send message",
                                on_click=call_send_message_click,
                            ),
                        ]
                    ),
                ],
                # horizontal_alignment="CENTER",
                vertical_alignment="START",
                horizontal_alignment="STRETCH",
            )
        )
        self.game_controller.start_game()

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
                vertical_alignment="CENTER",
                horizontal_alignment="CENTER",
            )
        )

        if self.page.route == "/prompts":
            self.setup_prompt()
        elif self.page.route == "/game":
            self.setup_game()
        elif self.page.route == "/loading":
            self.setup_loading()
        self.page.update()

    def view_pop(self, view):
        self.page.views.pop()
        top_view = self.page.views[-1]
        self.page.go(top_view.route)
