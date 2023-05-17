class GameController:
    def __init__(self, game_data_controller, page_controller):
        self.game_data_controller = game_data_controller
        self.page_controller = page_controller
        self.game_over = False

    def start_game(self):
        self.current_room = self.game_data_controller.first_room
        self.previous_room = None
        self.page_controller.add_message(self.game_data_controller.game_intro_text, False, False, True)

        while(not self.game_over):
            new_room = self.current_room.handover_control(self.page_controller, self.previous_room)
            if new_room == None:
                self.game_over = True
            self.previous_room = self.current_room
            self.current_room = new_room

        print("game over!")
