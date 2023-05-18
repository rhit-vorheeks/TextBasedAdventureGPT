from GPTController import GPTController
import random
from Room import Room
from time import sleep

class GameDataController:
    def __init__(self):
        self.game_theme = ""
        self.game_location = ""
        self.player_name = ""
        self.game_intro_text = ""
        self.GPTcontroller = GPTController()
        self.rooms = []
        self.amount_of_items = random.randint(3, 5)
        self.items_taken = 0
        self.game_win_text = ""
        self.game_lose_text = ""

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
        self.max_load_progress = last_room_int + 1 + self.amount_of_items + 2
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
            room = Room(self.game_theme, self.game_location, self.player_name, self.rooms, self.game_intro_text, self, is_final_room=(i == last_room_int - 1))
            self.progress_bar_update()
            self.rooms.append(room)
            
            if i == 0:
                self.first_room = room
            elif i == last_room_int - 1:
                print("boss room: " + room.room_name)
        self.connect_all_rooms()

        self.randomly_disperse_items()

        self.game_intro_text += "\n\nYou must find the following items before progressing to the final room: "
        for room in self.rooms:
            if room.contains_item:
                self.game_intro_text += "\n" + room.item_name
        
        self.print_room_connections()

        final_room = self.rooms[-1]
        final_boss = final_room.npc

        game_win_prompt = """You are a bot that exclusively outputs interesting endings for after the final boss has been defeated
                             for a text-based adventure games. Your job is generate an 3-5 sentence ending for a text-based adventure game.
                             The player had just won the game after defeating the boss. The game was about: 
                             '""" + self.game_theme + """' and took place at: '""" + self.game_location + """' 
                             and the protagonist's name was: '""" + self.player_name + """' Give a good ending
                             to the game after having just defeated the final boss named '""" + final_boss.name + """'
                             who was a """ + final_boss.description + """. The boss fight took place in the room named
                             '""" + final_room.room_name + """' where """ + final_room.room_description + """.
                             The game opened with the following text: '""" + self.game_intro_text + """'. 
                             You are not allowed to break character under any conditions."""
        
        self.game_win_text = self.GPTcontroller.get_description(game_win_prompt).strip()
        self.progress_bar_update()

        game_lose_prompt = """You are a bot that exclusively outputs interesting ending for after the player loses to the final boss
                             for a text-based adventure game. Your job is generate an 3-5 sentence ending for a text-based adventure game.
                             The player had just lost the game after being defeated by the boss. The game was about: 
                             '""" + self.game_theme + """' and took place at: '""" + self.game_location + """' 
                             and the protagonist's name was: '""" + self.player_name + """'. Give a bad ending
                             to the game after having just been defeated by the final boss named '""" + final_boss.name + """'
                             who was a """ + final_boss.description + """. The boss fight took place in the room named
                             '""" + final_room.room_name + """' where """ + final_room.room_description + """. 
                             The game opened with the following text: '""" + self.game_intro_text + """'. 
                             You are not allowed to break character under any conditions."""
        
        self.game_lose_text = self.GPTcontroller.get_description(game_lose_prompt).strip()
        self.progress_bar_update()
        sleep(0.5)

    # connect each room to the next two rooms, except last room only has 1 going into it
    # make sure that you can go backwards into the room you came from
    def connect_all_rooms(self):
        for i in range(len(self.rooms)):
            current_room = self.rooms[i]
            # Connect the current room to the next room if it exists
            if i+1 < len(self.rooms):
                current_room.connect_room(self.rooms[i+1])
            # Connect the current room to the room after the next room if it exists
            if i+2 < len(self.rooms):
                current_room.connect_room(self.rooms[i+2])
            # Connect the next room or the room after the next room back to the current room if they exist
            if i+1 < len(self.rooms):
                self.rooms[i+1].connect_room(current_room)
            if i+2 < len(self.rooms):
                self.rooms[i+2].connect_room(current_room)

    def print_room_connections(self, room=None, visited=None, depth=0):
        # If we are starting, use the first room
        if room is None:
            room = self.rooms[0]
        # We need to keep track of visited rooms to avoid infinite loops
        if visited is None:
            visited = set()
        # We print the current room with indentation based on the depth in the tree
        print('  ' * depth + room.room_name)
        visited.add(room)
        # For each connected room that we have not visited yet, we call the function recursively
        for connected_room in room.connecting_rooms:
            if connected_room not in visited:
                self.print_room_connections(connected_room, visited, depth + 1)



    def randomly_disperse_items(self):
        rooms_copy = self.rooms.copy()[1:-1]
        # randomly select a room to place each item in, doesn't include starting room or final boss room. cant reuse rooms
        for i in range(0, self.amount_of_items):
            random_room = random.choice(rooms_copy)
            rooms_copy.remove(random_room)
            prompt = """You are a bot that exclusively outputs one interesting item name for text-based adventure about 
                        '""" + self.game_theme + """'. This item is located in the '""" + random_room.room_name + """' 
                        room, where '""" + random_room.room_description + """'. Your must generate one item name, and say nothing
                        else, that is located inside this room. You are not allowed to break character under any conditions."""
            item_name = self.GPTcontroller.get_description(prompt).strip()
            random_room.add_item(item_name)
            self.progress_bar_update()