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

        
        self.page_controller.add_message("Type 'restart' to be brought back to the menu to start another adventure!", False, False, True)
        player_input = self.page_controller.wait_for_input()
        while(player_input.strip() != "restart"):
            self.page_controller.add_message("Unknown command!", False, False, True)
            player_input = self.page_controller.wait_for_input()

        self.page_controller.page.go("/prompts")
        print("game over!")
