import openai
import os


class GPTController:
    def __init__(self):
        # api_key = os.getenv('API_KEY')
        # openai.api_key = api_key
        
        # replace with your own API key if you'd like to run this yourself
        openai.api_key = "???"
    
    def get_dialogue(self, prompt):
        openai.Model.retrieve("gpt-3.5-turbo")
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        return completion.choices[0].message["content"]
    
    def get_description(self, prompt):
        response = openai.Completion.create(engine="text-davinci-003",
                                            prompt=prompt,
                                            temperature=1,
                                            max_tokens=1250,
                                            top_p=1,
                                            n=1,
                                            stream=False,
                                            frequency_penalty=1,
                                            presence_penalty=1,
                                            stop="")

        return response.choices[0].text
        
        # openai.Model.retrieve("gpt-3.5-turbo")
        # completion = openai.ChatCompletion.create(
        #     model="gpt-3.5-turbo",
        #     messages=[
        #         {"role": "user", "content": prompt}
        #     ]
        # )

        # return completion.choices[0].message["content"]