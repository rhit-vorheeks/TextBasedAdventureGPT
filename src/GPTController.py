import openai
import os
from dotenv import load_dotenv


class GPTController:
    def __init__(self):
        load_dotenv() # Load the environment variables from the .env file
        api_key = os.getenv('API_KEY') # Retrieve the API key from the environment variables
        openai.api_key = api_key # Set the API key for the OpenAI API
        

    def get_response(self, prompt):
        openai.Model.retrieve("gpt-3.5-turbo")
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        print(completion.choices[0].message)
        return completion.choices[0].message