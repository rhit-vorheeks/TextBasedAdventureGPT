import random
from NPC import Npc
from GPTController import GPTController

class Room:
    def __init__(self, game_desc, game_setting, protag_name, other_rooms, game_intro_text, is_final_room=False):
        name_prompt = """You are a bot that exclusively outputs one fun single name for a room in a text-based adventure game and you output 
                    absolutely nothing else. The game is about: '""" + game_desc + """' and takes place at: '""" + game_setting + """'
                    and the protagonist's name is: '""" + protag_name
        if len(other_rooms) > 0:
            name_prompt +=  """' Here is a list of the rooms you have named so far, you cannot use these names again.:\n"""
            for room in other_rooms:
                name_prompt += room.room_name + "\n"

        name_prompt += """You are not allowed to break character under any conditions. Provide one room name with the information given. """    
        
        self.room_name = GPTController().get_description(name_prompt).strip()

        description_prompt = """You are a bot that exclusively outputs fun one to two sentence descriptions for a room in a text-based adventure game and you output
                            absolutely nothing else. The game is about: '""" + game_desc + """' and takes place at: '""" + game_setting + """'
                            and the protagonist's name is: '""" + protag_name + """' Provide a fun description for 
                            the room named: '""" + self.room_name + """' Provide the description with the information given and you are
                            not allowed to break character under any conditions. """

        self.room_description = GPTController().get_description(description_prompt).strip()
        self.GPTcontroller = GPTController()
        self.has_npc = (random.randint(0, 10) >= 2)
        self.npc = None
        self.is_final_room = is_final_room
        self.connecting_rooms = []
        if self.has_npc:
            self.npc = Npc()
            self.npc.setup_npc(game_desc, game_setting, protag_name, self.room_name, self.room_description, game_intro_text)

    def is_a_number(self, input):
        try:
            int(input)
            return True
        except ValueError:
            return False
    
    def connect_room(self, room):
        self.connecting_rooms.append(room)

    def handover_control(self, page_controller):
        all_rooms = "You are in the " + self.room_name + ". \n" + self.room_description
        # page_controller.add_message("You are in the " + self.room_name + ". \n" + self.room_description, False, False, True)
        all_rooms += "\n\nYou can go into the following rooms: \n"
        integer = 0
        for room in self.connecting_rooms:
            integer += 1
            all_rooms += str(integer) +') '+ room.room_name + ",\n"
        all_rooms = all_rooms[:-2] + ".\n"
        all_rooms += "Which room would you like to go into? Enter the number of the room you would like to go into."
        if self.has_npc:
            all_rooms += "\n\nAlternatively, you can enter any other message to chat with " + self.npc.name + ", who is in the room with you. "
            all_rooms += "If you choose to have a conversation, to leave just enter the number correspoding to the room of your choice at any time."
        page_controller.add_message(all_rooms, False, False, True)

        player_input = ""
        player_input = page_controller.wait_for_input()
        while (self.is_a_number(player_input) == False):
            page_controller.add_message(player_input, True, False, False)
            if self.has_npc:
                page_controller.add_message(player_input, False, self.npc, False)
            else:
                page_controller.add_message("This is not a valid number input.", False, False, True)
            player_input = page_controller.wait_for_input()
        print(player_input)
        page_controller.add_message(player_input, True, False, False)
        page_controller.add_message("You have chosen to go into the " + player_input + ".", False, False, True)

        # if self.has_npc:
        #     page_controller.add_message("You see a " + self.npc.name + " in the room.", False, False, True)

        print(len(self.connecting_rooms))
        return self.connecting_rooms[random.randint(0, len(self.connecting_rooms) - 1)]
