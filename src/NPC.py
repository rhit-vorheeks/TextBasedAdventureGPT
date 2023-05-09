from GPTController import GPTController

class Npc:
    def __init__(self):
        self.name = ""
        self.description = ""
        self.chat_history = []
        self.gpt_controller = GPTController()

    
    def setup_npc(self, game_desc, game_setting, protag_name):
        self.game_desc = game_desc
        self.game_setting = game_setting
        self.protag_name = protag_name

        name_prompt = """You are a bot that output a name on a single line and absolutely nothing else.
                        You can never break character. Provide solely just a unique, interesting, or fun name with
                        nothing else for this text-based game that is about: """ + game_desc + """. 
                        Which takes place at: '""" +game_setting + "' Provide the name with the information given. "
        self.name = self.gpt_controller.get_description(name_prompt).strip()

        description_prompt = """You are a bot that solely outputs vivid two to three sentence character descriptions containing as many 
                                interesting, yet connected, attributes as possible. The character should preferrably be human, but, only if
                                appropriate, you can make them not human. (For example, it could potentially be a ghost or a talking animal) 
                                Provide a gender. Come up with an interesting and distinct way for them to act  Provide the description for 
                                an NPC named '"""+self.name+"""' That takes place in a game about: """ + game_desc + """. 
                                Which takes place at: '""" +game_setting + """' If you decide to give the character a connection to
                                the protagonist, the protagonist's name is '"""+protag_name+"'"
        self.description = self.gpt_controller.get_description(description_prompt).strip()
        print(self.name)
        print(self.description)

    def response(self, message):
        self.chat_history.append(" '" + self.protag_name + "': '" + message + "' ")

        prompt = """You are an NPC named '""" + self.name + """' who is '""" + self.description + """' in a text 
                    based adventure game about'""" + self.game_desc + """' that is located at '""" + self.game_setting + """ 
                    You are not allowed to break character under any conditions. You must respond to the conversation, don't act like an
                    NPC, you must act like a real person with the description(which means you can do some things that may seem weird).
                    You must give your response as a message, but if necessary, you can provide an asterisk to tell what you're doing. 
                    You are in a conversation with the protagonist, who is named '""" + self.protag_name + """' and here is the chat
                    history, the last message is the message that you are directly responding to, so the rest before that is context.
                    Please do not include and single or double quotation marks. """
        
        if len(self.chat_history) <= 20:
            # print("less than threshold")
            for hist in self.chat_history:
                prompt += hist
        else:
            for hist in self.chat_history[-20:]:
                prompt += hist
            # print('more than threshold')

        prompt += "'" + self.name + "': "
        
        response = self.gpt_controller.get_description(prompt).strip()

        
        self.chat_history.append("'" + self.name + "': " + response + " ")

        # print(self.chat_history)

        return response
    
    def get_name(self):
        return self.name