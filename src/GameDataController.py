from GPTController import GPTController
import random
from Room import Room

class GameDataController:
    def __init__(self):
        self.game_theme = ""
        self.game_location = ""
        self.player_name = ""
        self.game_intro_text = ""
        self.GPTcontroller = GPTController()
        self.rooms = []

    def set_game_theme(self, theme):
        self.game_theme = theme.strip()

    def set_game_location(self, location):
        self.game_location = location.strip()

    def set_player_name(self, name):
        self.player_name = name.strip()

    def get_game_theme(self):
        return self.game_theme
    
    def get_game_location(self):
        return self.game_location
    
    def get_player_name(self):
        return self.player_name
    
    def progress_bar_update(self):
        self.load_progress += 1
        self.loading_circle.value = self.load_progress / self.max_load_progress
        self.page.update()

    def generate_game_dataset(self, loading_circle, page):
        self.load_progress = 0
        self.page = page
        # last_room_int = random.randint(12, 15)
        last_room_int = 8
        self.max_load_progress = last_room_int + 1
        self.loading_circle = loading_circle
        self.rooms = []

        game_intro_prompt = """You are a bot that exclusively outputs interesting openings for text-based adventure 
                                games. Your job is generate an 3-5 sentence opening for a text-based adventure game. The game is 
                                about: '""" + self.game_theme + """' and takes place at: '""" + self.game_location + """' 
                                and the protagonist's name is: '""" + self.player_name + """' You are not allowed to break
                                character under any conditions. """
        self.game_intro_text = self.GPTcontroller.get_description(game_intro_prompt).strip()
        self.progress_bar_update()

        for i in range(0, last_room_int):
            room = Room(self.game_theme, self.game_location, self.player_name, self.rooms, self.game_intro_text, is_final_room=(i == last_room_int - 1))
            self.progress_bar_update()
            self.rooms.append(room)
            
            if i == 0:
                self.first_room = room
            elif i == last_room_int - 1:
                print("boss room: " + room.room_name)
        self.randomly_connect_all_rooms()

        #prints all room connections
        for room in self.rooms:
            print(room.room_name)
            print(room.connecting_rooms)
            print()

    # randomly connect each room to two-three other rooms. ensure that final room is connected to a single room.
    def randomly_connect_all_rooms(self):
        # Shuffle the rooms except for the last one (the boss room)
        non_boss_rooms = self.rooms[:-1]
        random.shuffle(non_boss_rooms)

        # Connect the rooms in the shuffled order
        for i in range(len(non_boss_rooms) - 1):
            # Connect each room to the next one
            non_boss_rooms[i].connect_room(non_boss_rooms[i + 1])

            # Randomly connect each room to one other random room, ensuring it's not the same room or the next one
            other_room = random.choice(non_boss_rooms[:i] + non_boss_rooms[i + 2:])
            non_boss_rooms[i].connect_room(other_room)

        # Connect the last room in the shuffled list to the boss room
        non_boss_rooms[-1].connect_room(self.rooms[-1])

        # Make sure the boss room only connects back to the last room in the shuffled list
        self.rooms[-1].connect_room(non_boss_rooms[-1])
