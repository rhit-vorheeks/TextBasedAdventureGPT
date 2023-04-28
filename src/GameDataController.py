from GPTController import GPTController

class GameDataController:
    def __init__(self):
        self.game_theme = ""
        self.game_location = ""
        self.player_name = ""
        self.GPTcontroller = GPTController()

    def set_game_theme(self, theme):
        self.game_theme = theme

    def set_game_location(self, location):
        self.game_location = location

    def set_player_name(self, name):
        self.player_name = name

    def get_game_theme(self):
        return self.game_theme
    
    def get_game_location(self):
        return self.game_location
    
    def get_player_name(self):
        return self.player_name
    
    def generate_game_dataset(self):
        return ""
