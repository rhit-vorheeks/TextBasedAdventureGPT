import openai
import os
from dotenv import load_dotenv


class GPTController:
    def __init__(self):
        load_dotenv()
        api_key = os.getenv('API_KEY')
        openai.api_key = api_key
        

    def get_dialogue(self, prompt):
        openai.Model.retrieve("gpt-3.5-turbo")
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        return completion.choices[0].message["content"]