import random
from NPC import Npc
from GPTController import GPTController

class Room:
    def __init__(self, game_desc, game_setting, protag_name, other_rooms, game_intro_text, game_data_controller, is_final_room=False):
        name_prompt = """You are a bot that exclusively outputs one fun single name for a room in a text-based adventure game and you output 
                    absolutely nothing else. The game is about: '""" + game_desc + """' and takes place at: '""" + game_setting + """'
                    and the protagonist's name is: '""" + protag_name
        if len(other_rooms) > 0:
            name_prompt +=  """' Here is a list of the rooms you have named so far, you cannot use these names again.:\n"""
            for room in other_rooms:
                name_prompt += room.room_name + "\n"

        if is_final_room:
            name_prompt += """' This is the final room of the game, which contains the final boss. """

        name_prompt += """You are not allowed to break character under any conditions. Provide one room name with the information given. """    
        
        self.room_name = GPTController().get_description(name_prompt).strip()

        description_prompt = """You are a bot that exclusively outputs fun one to two sentence descriptions for a room in a text-based adventure game and you output
                            absolutely nothing else. The game is about: '""" + game_desc + """' and takes place at: '""" + game_setting + """'
                            and the protagonist's name is: '""" + protag_name + """' Provide a fun description for 
                            the room named: '""" + self.room_name
        
        
        if is_final_room:
            description_prompt += """' This is the final room of the game, which contains the final boss. """

        description_prompt += """' Provide the description with the information given and you are not allowed to break character under any conditions. """

        self.room_description = GPTController().get_description(description_prompt).strip()
        self.GPTcontroller = GPTController()
        self.has_npc = (random.randint(0, 10) >= 2)
        self.is_final_room = is_final_room
        if self.is_final_room:
            self.has_npc = True
        self.npc = None
        self.connecting_rooms = []
        self.contains_item = False
        self.item_name = ""
        self.item_taken = False
        self.game_data_controller = game_data_controller
        if self.has_npc:
            self.npc = Npc(is_final_room)
            self.npc.setup_npc(game_desc, game_setting, protag_name, self.room_name, self.room_description, game_intro_text)

    def add_item(self, item_name):
        self.contains_item = True
        self.item_name = item_name

    def is_a_number(self, input):
        try:
            int(input)
            return True
        except ValueError:
            return False
    
    def connect_room(self, room):
        self.connecting_rooms.append(room)

    def handover_control(self, page_controller, prev_room):
        all_rooms = "You are in the " + self.room_name + ". \n" + self.room_description

    # Check if this is the final room and player has collected all the items
        if self.is_final_room and self.game_data_controller.amount_of_items == self.game_data_controller.items_taken:
            all_rooms += "\n\nThis is the final room and you have collected all the items. Prepare for a boss fight!"
            page_controller.add_message(all_rooms, False, False, True)
            
            # Initialize boss and player health
            boss_health = 100
            player_health = 100

            # Boss fight
            while boss_health > 0 and player_health > 0:
                page_controller.add_message(f"{self.npc.name} health: {boss_health}. Your health: {player_health}.", False, False, True)
                page_controller.add_message(f"What do you do? (type 'attack' to attack, 'defend' to defend, or anything else to talk to {self.npc.name})", False, False, True)
                player_input = page_controller.wait_for_input()
                
                page_controller.add_message(player_input, True, False, False)

                player_input = player_input.lower()

                reduced_damage = 0
                if player_input == 'attack':
                    damage = random.randint(15, 25)
                    boss_health -= damage
                    page_controller.add_message(f"You attacked {self.npc.name} and dealt {damage} damage!", False, False, True)
                elif player_input == 'defend':
                    # Defending reduces the damage taken from the boss's next attack
                    reduced_damage += random.randint(10, 20)
                    heal_amount = random.randint(10, 40)
                    if player_health + heal_amount > 100:
                        heal_amount = 100 - player_health
                    player_health += heal_amount
                    text_message = f"You defended against {self.npc.name}'s attack. You stop {reduced_damage} worth of damage."
                    text_message += f"\n\nYou also heal {heal_amount} health."
                    page_controller.add_message(text_message, False, False, True)
                else:
                    # page_controller.add_message("Invalid action. The boss attacks you!", False, False, True)
                    
                    page_controller.add_message(player_input, False, self.npc, False)
                    continue

                # Boss attacks player and deals a random amount of damage
                if boss_health > 0:
                    damage = random.randint(20, 35) - reduced_damage
                    player_health -= damage
                    page_controller.add_message(f"{self.npc.name} attacked you and dealt {damage} damage!", False, False, True)

            # Determine the result of the fight
            if player_health <= 0:
                # page_controller.add_message(f"You have been defeated by {self.npc.name}. Game over!", False, False, True)
                page_controller.add_message(self.game_data_controller.game_lose_text, False, False, True)
            elif boss_health <= 0:
                # page_controller.add_message(f"You defeated {self.npc.name}! Congratulations, you've completed the game!", False, False, True)
                page_controller.add_message(self.game_data_controller.game_win_text, False, False, True)
            return None

        elif self.is_final_room and self.game_data_controller.amount_of_items != self.game_data_controller.items_taken:
            all_rooms += "\n\nThis is the final room but you have not collected all the items. You cannot proceed to the boss room yet."
            all_rooms += "\n\nYou have collected " + str(self.game_data_controller.items_taken) + " out of " + str(self.game_data_controller.amount_of_items) + " items."
            all_rooms += "\nReturning to the previous room..."
            page_controller.add_message(all_rooms, False, False, True)
            return prev_room
        else:

            if self.contains_item and not self.item_taken:
                all_rooms += "\n\nYou see '" + self.item_name + "' in the room and collect it."
                self.item_taken = True
                self.game_data_controller.items_taken += 1

            # page_controller.add_message("You are in the " + self.room_name + ". \n" + self.room_description, False, False, True)
            all_rooms += "\n\nYou can go into the following rooms: \n"

            integer = 0
            room_storage = {}
            for room in self.connecting_rooms:
                integer += 1
                all_rooms += str(integer) +') '+ room.room_name + ",\n"
                room_storage[str(integer)] = room
                
            all_rooms = all_rooms[:-2] + ".\n"
            all_rooms += "\nWhich room would you like to go into? Enter the number of the room you would like to go into."
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
            page_controller.add_message("You have chosen to go into room #" + player_input + ".", False, False, True)

            # if self.has_npc:
            #     page_controller.add_message("You see a " + self.npc.name + " in the room.", False, False, True)

            print(len(self.connecting_rooms))
            return room_storage[player_input]
